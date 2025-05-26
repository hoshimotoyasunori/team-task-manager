from django.core.management.base import BaseCommand
from api.models import Estimate, Case, User
import random
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'ダミーのEstimateデータを作成します'

    def handle(self, *args, **options):
        cases = list(Case.objects.all())
        users = list(User.objects.all())
        if not cases or not users:
            self.stdout.write(self.style.ERROR('Case, Userのダミーデータを先に作成してください'))
            return
        dummy_data = [
            {
                'case': random.choice(cases),
                'created_date': date.today() - timedelta(days=5),
                'valid_until': date.today() + timedelta(days=25),
                'total_amount': 1200000,
                'approval_status': 'Pending',
                'approver': random.choice(users),
                'approval_date': None,
            },
            {
                'case': random.choice(cases),
                'created_date': date.today() - timedelta(days=15),
                'valid_until': date.today() + timedelta(days=15),
                'total_amount': 800000,
                'approval_status': 'Approved',
                'approver': random.choice(users),
                'approval_date': date.today() - timedelta(days=1),
            },
        ]
        for data in dummy_data:
            Estimate.objects.get_or_create(
                case=data['case'],
                created_date=data['created_date'],
                defaults={
                    'valid_until': data['valid_until'],
                    'total_amount': data['total_amount'],
                    'approval_status': data['approval_status'],
                    'approver': data['approver'],
                    'approval_date': data['approval_date'],
                }
            )
        self.stdout.write(self.style.SUCCESS('ダミーEstimateデータを作成しました')) 