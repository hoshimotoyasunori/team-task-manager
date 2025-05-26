from django.core.management.base import BaseCommand
from api.models import Schedule, Case, User
import random
from datetime import date, timedelta, time

class Command(BaseCommand):
    help = 'ダミーのScheduleデータを作成します'

    def handle(self, *args, **options):
        cases = list(Case.objects.all())
        users = list(User.objects.all())
        if not cases or not users:
            self.stdout.write(self.style.ERROR('Case, Userのダミーデータを先に作成してください'))
            return
        dummy_data = [
            {
                'case': random.choice(cases),
                'assigned_to': random.choice(users),
                'schedule_date': date.today() + timedelta(days=3),
                'start_time': time(10, 0),
                'end_time': time(12, 0),
                'type': 'Appointment',
                'location': '現地',
                'details': '調査アポイント',
            },
            {
                'case': random.choice(cases),
                'assigned_to': random.choice(users),
                'schedule_date': date.today() + timedelta(days=7),
                'start_time': time(14, 0),
                'end_time': time(16, 0),
                'type': 'Construction',
                'location': '現地',
                'details': '施工予定',
            },
        ]
        for data in dummy_data:
            Schedule.objects.get_or_create(
                case=data['case'],
                assigned_to=data['assigned_to'],
                schedule_date=data['schedule_date'],
                start_time=data['start_time'],
                defaults={
                    'end_time': data['end_time'],
                    'type': data['type'],
                    'location': data['location'],
                    'details': data['details'],
                }
            )
        self.stdout.write(self.style.SUCCESS('ダミーScheduleデータを作成しました')) 