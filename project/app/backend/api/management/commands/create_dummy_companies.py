from django.core.management.base import BaseCommand
from api.models import Company

class Command(BaseCommand):
    help = 'ダミーのCompanyデータを作成します'

    def handle(self, *args, **options):
        dummy_data = [
            {'name': '東京不動産', 'contact_info': {'tel': '03-1111-2222', 'email': 'tokyo@example.com'}, 'address': '東京都中央区1-1-1', 'contact_person_name': '田中一郎'},
            {'name': '大阪管理', 'contact_info': {'tel': '06-3333-4444', 'email': 'osaka@example.com'}, 'address': '大阪市北区2-2-2', 'contact_person_name': '山本花子'},
            {'name': '名古屋エステート', 'contact_info': {'tel': '052-5555-6666', 'email': 'nagoya@example.com'}, 'address': '名古屋市中区3-3-3', 'contact_person_name': '鈴木次郎'},
        ]
        for data in dummy_data:
            Company.objects.get_or_create(name=data['name'], defaults={
                'contact_info': data['contact_info'],
                'address': data['address'],
                'contact_person_name': data['contact_person_name'],
            })
        self.stdout.write(self.style.SUCCESS('ダミーCompanyデータを作成しました')) 