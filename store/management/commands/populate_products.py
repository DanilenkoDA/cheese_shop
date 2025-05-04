from django.core.management.base import BaseCommand
import json
from store.models import Product

class Command(BaseCommand):
    help = 'Populate the product table with initial data from JSON file'

    def handle(self, *args, **kwargs):
        # Откройте файл JSON
        with open('store/products.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Пройдем по данным и создадим объекты в базе данных
        for item in data:
            fields = item['fields']
            product = Product(
                name=fields['name'],
                description=fields['description'],
                price=fields['price'],
                image=fields['image']
            )
            product.save()

        self.stdout.write(self.style.SUCCESS('Products populated successfully!'))
