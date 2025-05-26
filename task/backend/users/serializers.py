from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'profile_image', 'bio', 'department', 'notify_email')
        read_only_fields = ('id', 'username', 'email')

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User.notifications.rel.related_model
        fields = ('id', 'message', 'is_read', 'created_at', 'link')

class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = User.activity_logs.rel.related_model
        fields = ('id', 'action', 'created_at', 'related_task_id') 