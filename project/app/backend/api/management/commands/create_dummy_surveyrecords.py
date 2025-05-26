from django.core.management.base import BaseCommand
from api.models import SurveyRecord, Case, User
import random
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'ダミーのSurveyRecordデータを作成します'

    def handle(self, *args, **options):
        cases = list(Case.objects.all())
        users = list(User.objects.all())
        if not cases or not users:
            self.stdout.write(self.style.ERROR('Case, Userのダミーデータを先に作成してください'))
            return
        dummy_data = [
            {
                'survey_date': date.today() - timedelta(days=3),
                'assigned_to': random.choice(users),
                'summary': '配管保全機器の設置前点検',
                'details': '点検の結果、特に問題なし。',
                'attachment_paths': ['photo1.jpg', 'photo2.jpg'],
            },
            {
                'survey_date': date.today() - timedelta(days=10),
                'assigned_to': random.choice(users),
                'summary': '貯水槽清掃前の現地調査',
                'details': '一部汚れあり、清掃推奨。',
                'attachment_paths': ['photo3.jpg'],
            },
        ]
        for case in cases:
            for data in dummy_data:
                SurveyRecord.objects.get_or_create(
                    case=case,
                    survey_date=data['survey_date'],
                    defaults={
                        'assigned_to': data['assigned_to'],
                        'summary': data['summary'],
                        'details': data['details'],
                        'attachment_paths': data['attachment_paths'],
                    }
                )
        self.stdout.write(self.style.SUCCESS('ダミーSurveyRecordデータを作成しました')) 