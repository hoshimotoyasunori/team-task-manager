from django.core.management.base import BaseCommand
from api.models import Property, Company, Owner
import random

class Command(BaseCommand):
    help = 'ダミーのPropertyデータを作成します'

    def handle(self, *args, **options):
        companies = list(Company.objects.all())
        owners = list(Owner.objects.all())
        if not companies or not owners:
            self.stdout.write(self.style.ERROR('先にCompanyとOwnerのダミーデータを作成してください'))
            return
        dummy_data = [
            {'address': '東京都中央区A-1', 'property_type': 'Apartment', 'year_built': 2000, 'company': random.choice(companies), 'owner': random.choice(owners)},
            {'address': '大阪市北区B-2', 'property_type': 'House', 'year_built': 1995, 'company': random.choice(companies), 'owner': random.choice(owners)},
            {'address': '名古屋市中区C-3', 'property_type': 'Apartment', 'year_built': 2010, 'company': random.choice(companies), 'owner': random.choice(owners)},
        ]
        for data in dummy_data:
            Property.objects.get_or_create(address=data['address'], defaults={
                'property_type': data['property_type'],
                'year_built': data['year_built'],
                'company': data['company'],
                'owner': data['owner'],
            })
        self.stdout.write(self.style.SUCCESS('ダミーPropertyデータを作成しました')) 