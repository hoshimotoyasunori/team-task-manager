from django.core.management.base import BaseCommand
from api.models import ContractItem, Contract
import random

class Command(BaseCommand):
    help = 'ダミーのContractItemデータを作成します'

    def handle(self, *args, **options):
        contracts = list(Contract.objects.all())
        if not contracts:
            self.stdout.write(self.style.ERROR('Contractのダミーデータを先に作成してください'))
            return
        dummy_items = [
            {'item_name': '配管保全機器設置', 'quantity': 2, 'unit_price': 500000},
            {'item_name': '貯水槽清掃', 'quantity': 1, 'unit_price': 200000},
            {'item_name': '排水管清掃工事', 'quantity': 3, 'unit_price': 150000},
            {'item_name': '給水ポンプ切替', 'quantity': 1, 'unit_price': 300000},
        ]
        for contract in contracts:
            for item in random.sample(dummy_items, k=2):
                subtotal = item['quantity'] * item['unit_price']
                ContractItem.objects.get_or_create(
                    contract=contract,
                    item_name=item['item_name'],
                    defaults={
                        'quantity': item['quantity'],
                        'unit_price': item['unit_price'],
                        'subtotal': subtotal,
                    }
                )
        self.stdout.write(self.style.SUCCESS('ダミーContractItemデータを作成しました')) 