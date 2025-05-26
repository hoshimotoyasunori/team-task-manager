from django.core.management.base import BaseCommand
from api.models import User

class Command(BaseCommand):
    help = 'ダミーのUserデータを作成します'

    def handle(self, *args, **options):
        dummy_data = [
            {'employee_number': '1001', 'username': 'sales1', 'email': 'sales1@example.com', 'role': 'Sales', 'status': 'Active', 'is_first_login': True},
            {'employee_number': '1002', 'username': 'sales2', 'email': 'sales2@example.com', 'role': 'Sales', 'status': 'Active', 'is_first_login': True},
            {'employee_number': '2001', 'username': 'hq1', 'email': 'hq1@example.com', 'role': 'HQ', 'status': 'Active', 'is_first_login': True},
        ]
        for data in dummy_data:
            User.objects.get_or_create(employee_number=data['employee_number'], defaults=data)
        self.stdout.write(self.style.SUCCESS('ダミーUserデータを作成しました')) 