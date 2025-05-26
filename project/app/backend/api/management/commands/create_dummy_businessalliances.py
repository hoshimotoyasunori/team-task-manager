from django.core.management.base import BaseCommand
from api.models import BusinessAlliance, Company
import random
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'ダミーのBusinessAllianceデータを作成します'

    def handle(self, *args, **options):
        companies = list(Company.objects.all())
        if len(companies) < 2:
            self.stdout.write(self.style.ERROR('BusinessAlliance作成には2社以上のCompanyデータが必要です'))
            return
        dummy_data = [
            {'company': companies[0], 'start_date': date.today() - timedelta(days=365), 'referral_commission_rate': 5.0, 'contract_info': '契約書A'},
            {'company': companies[1], 'start_date': date.today() - timedelta(days=200), 'referral_commission_rate': 7.5, 'contract_info': '契約書B'},
        ]
        for data in dummy_data:
            BusinessAlliance.objects.get_or_create(company=data['company'], defaults={
                'start_date': data['start_date'],
                'referral_commission_rate': data['referral_commission_rate'],
                'contract_info': data['contract_info'],
            })
        self.stdout.write(self.style.SUCCESS('ダミーBusinessAllianceデータを作成しました')) 