from django.core.management.base import BaseCommand
from api.models import ConstructionType

class Command(BaseCommand):
    help = 'ダミーのConstructionTypeデータを作成します'

    def handle(self, *args, **options):
        dummy_data = [
            {'name': '配管保全機器取り付け'},
            {'name': '貯水槽清掃'},
            {'name': '排水管清掃工事'},
            {'name': '給水ポンプ切替'},
            {'name': '防水工事'},
            {'name': '外壁工事'},
        ]
        for data in dummy_data:
            ConstructionType.objects.get_or_create(name=data['name'])
        self.stdout.write(self.style.SUCCESS('ダミーConstructionTypeデータを作成しました')) 