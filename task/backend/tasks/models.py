from django.db import models
from django.contrib.auth import get_user_model

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    assignee = models.ForeignKey(get_user_model(), related_name='assigned_tasks', on_delete=models.SET_NULL, null=True, blank=True)
    creator = models.ForeignKey(get_user_model(), related_name='created_tasks', on_delete=models.CASCADE)
    due_date = models.DateField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    project = models.ForeignKey('Project', related_name='tasks', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(
        max_length=50,
        choices=[
            ('not_started', '未着手'),
            ('in_progress', '進行中'),
            ('review', 'レビュー待ち'),
            ('done', '完了'),
        ],
        default='not_started'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
