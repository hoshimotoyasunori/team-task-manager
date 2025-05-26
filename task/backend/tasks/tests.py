from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Task

User = get_user_model()

class TaskAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='taskuser', password='taskpass123')
        self.client.force_authenticate(user=self.user)

    def test_create_task(self):
        url = reverse('task-list-create')
        data = {
            'title': 'Test Task',
            'description': 'Test Description',
            'assignee': self.user.id,
            'creator': self.user.id,
            'status': 'todo'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Task.objects.filter(title='Test Task').exists())

    def test_get_task_list(self):
        Task.objects.create(title='Task1', assignee=self.user, creator=self.user, status='todo')
        url = reverse('task-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_update_task(self):
        task = Task.objects.create(title='Task2', assignee=self.user, creator=self.user, status='todo')
        url = reverse('task-detail', args=[task.id])
        data = {'title': 'Task2 Updated', 'status': 'doing'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.title, 'Task2 Updated')
        self.assertEqual(task.status, 'doing')

    def test_delete_task(self):
        task = Task.objects.create(title='Task3', assignee=self.user, creator=self.user, status='todo')
        url = reverse('task-detail', args=[task.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=task.id).exists())
