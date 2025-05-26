from django.core.management.base import BaseCommand
from api.models import Case, Property, Owner, User, ConstructionType
import random
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'ダミーのCaseデータを作成します'

    def handle(self, *args, **options):
        properties = list(Property.objects.all())
        owners = list(Owner.objects.all())
        users = list(User.objects.all())
        construction_types = list(ConstructionType.objects.all())
        if not properties or not owners or not users or not construction_types:
            self.stdout.write(self.style.ERROR('Property, Owner, User, ConstructionTypeのダミーデータを先に作成してください'))
            return
        dummy_data = [
            {
                'owner': random.choice(owners),
                'property': random.choice(properties),
                'assigned_sales': random.choice(users),
                'case_type': 'New',
                'status': 'Appointment',
                'occurence_date': date.today() - timedelta(days=30),
            },
            {
                'owner': random.choice(owners),
                'property': random.choice(properties),
                'assigned_sales': random.choice(users),
                'case_type': 'CS',
                'status': 'Surveyed',
                'occurence_date': date.today() - timedelta(days=10),
            },
        ]
        for data in dummy_data:
            case, created = Case.objects.get_or_create(
                owner=data['owner'],
                property=data['property'],
                assigned_sales=data['assigned_sales'],
                case_type=data['case_type'],
                status=data['status'],
                occurence_date=data['occurence_date'],
            )
            if created:
                # ManyToManyの想定工事種別をランダムで1つ紐付け
                case.expected_construction_types.set([random.choice(construction_types)])
        self.stdout.write(self.style.SUCCESS('ダミーCaseデータを作成しました')) 