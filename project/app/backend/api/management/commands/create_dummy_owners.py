from django.core.management.base import BaseCommand
from api.models import Owner

class Command(BaseCommand):
    help = 'ダミーのOwnerデータを作成します'

    def handle(self, *args, **options):
        dummy_data = [
            {'name': '山田太郎', 'contact_info': {'email': 'taro@example.com', 'tel': '090-1111-2222'}, 'address': '東京都新宿区1-1-1'},
            {'name': '佐藤花子', 'contact_info': {'email': 'hanako@example.com', 'tel': '080-3333-4444'}, 'address': '東京都渋谷区2-2-2'},
            {'name': '鈴木一郎', 'contact_info': {'email': 'ichiro@example.com', 'tel': '070-5555-6666'}, 'address': '東京都港区3-3-3'},
        ]
        for data in dummy_data:
            Owner.objects.get_or_create(name=data['name'], defaults={
                'contact_info': data['contact_info'],
                'address': data['address'],
            })
        self.stdout.write(self.style.SUCCESS('ダミーOwnerデータを作成しました')) 