from django.core.management.base import BaseCommand
from api.models import ReportRecord, Case, User
import random
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'ダミーのReportRecordデータを作成します'

    def handle(self, *args, **options):
        cases = list(Case.objects.all())
        users = list(User.objects.all())
        if not cases or not users:
            self.stdout.write(self.style.ERROR('Case, Userのダミーデータを先に作成してください'))
            return
        dummy_data = [
            {
                'report_date': date.today() - timedelta(days=2),
                'assigned_to': random.choice(users),
                'negotiation_content': '見積内容の説明と契約条件の確認を実施。',
                'result': 'Won',
            },
            {
                'report_date': date.today() - timedelta(days=8),
                'assigned_to': random.choice(users),
                'negotiation_content': '価格交渉の結果、継続検討となった。',
                'result': 'Ongoing',
            },
        ]
        for case in cases:
            for data in dummy_data:
                ReportRecord.objects.get_or_create(
                    case=case,
                    report_date=data['report_date'],
                    defaults={
                        'assigned_to': data['assigned_to'],
                        'negotiation_content': data['negotiation_content'],
                        'result': data['result'],
                    }
                )
        self.stdout.write(self.style.SUCCESS('ダミーReportRecordデータを作成しました')) 