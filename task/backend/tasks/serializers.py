from rest_framework import serializers
from .models import Task, Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    assignee_name = serializers.SerializerMethodField()
    project_name = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = '__all__'
        extra_fields = ['project_name']

    def get_assignee_name(self, obj):
        return obj.assignee.username if obj.assignee else None

    def get_creator(self, obj):
        return obj.creator.username if obj.creator else None

    def get_project_name(self, obj):
        return obj.project.name if obj.project else None

    def get_assignee(self, obj):
        return obj.assignee.username if obj.assignee else None 