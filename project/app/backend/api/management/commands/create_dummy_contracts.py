from django.core.management.base import BaseCommand
from api.models import Contract, Case, Estimate, User
import random
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'ダミーのContractデータを作成します'

    def handle(self, *args, **options):
        cases = list(Case.objects.all())
        estimates = list(Estimate.objects.all())
        users = list(User.objects.all())
        if not cases or not estimates or not users:
            self.stdout.write(self.style.ERROR('Case, Estimate, Userのダミーデータを先に作成してください'))
            return
        dummy_data = [
            {
                'case': random.choice(cases),
                'estimate': random.choice(estimates),
                'contract_type': 'Order',
                'contract_date': date.today() - timedelta(days=3),
                'contract_amount': 1200000,
                'desired_construction_date': date.today() + timedelta(days=10),
                'payment_terms': '一括払い',
                'owner_sign_date': date.today() - timedelta(days=2),
                'approval_status': 'Pending',
                'approver': random.choice(users),
                'approval_date': None,
                'customer_confirmation_status': 'Required',
                'customer_confirmation_date': None,
                'customer_confirmation_by': random.choice(users),
            },
            {
                'case': random.choice(cases),
                'estimate': random.choice(estimates),
                'contract_type': 'Contract',
                'contract_date': date.today() - timedelta(days=7),
                'contract_amount': 800000,
                'desired_construction_date': date.today() + timedelta(days=5),
                'payment_terms': '分割払い',
                'owner_sign_date': date.today() - timedelta(days=6),
                'approval_status': 'Approved',
                'approver': random.choice(users),
                'approval_date': date.today() - timedelta(days=1),
                'customer_confirmation_status': 'CompletedOK',
                'customer_confirmation_date': date.today(),
                'customer_confirmation_by': random.choice(users),
            },
        ]
        for data in dummy_data:
            Contract.objects.get_or_create(
                case=data['case'],
                estimate=data['estimate'],
                contract_type=data['contract_type'],
                contract_date=data['contract_date'],
                defaults={
                    'contract_amount': data['contract_amount'],
                    'desired_construction_date': data['desired_construction_date'],
                    'payment_terms': data['payment_terms'],
                    'owner_sign_date': data['owner_sign_date'],
                    'approval_status': data['approval_status'],
                    'approver': data['approver'],
                    'approval_date': data['approval_date'],
                    'customer_confirmation_status': data['customer_confirmation_status'],
                    'customer_confirmation_date': data['customer_confirmation_date'],
                    'customer_confirmation_by': data['customer_confirmation_by'],
                }
            )
        self.stdout.write(self.style.SUCCESS('ダミーContractデータを作成しました')) 