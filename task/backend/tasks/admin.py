from django.contrib import admin
from .models import Task, Project

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'assignee', 'creator', 'created_at', 'updated_at')
    list_filter = ('status', 'assignee', 'creator', 'created_at')
    search_fields = ('title', 'description', 'assignee__username', 'creator__username')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name', 'description')
