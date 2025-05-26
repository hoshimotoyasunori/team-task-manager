from django.contrib import admin
from .models import User, Notification, ActivityLog

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'department', 'notify_email', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'department')
    list_filter = ('is_staff', 'is_superuser', 'department')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at', 'link')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'message')

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'created_at', 'related_task_id')
    list_filter = ('created_at', 'user')
    search_fields = ('user__username', 'action', 'related_task_id')
