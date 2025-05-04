from django.core.management.base import BaseCommand
from store.models import Product

class Command(BaseCommand):
    help = 'Delete all products'

    def handle(self, *args, **kwargs):
        Product.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All products deleted.'))
