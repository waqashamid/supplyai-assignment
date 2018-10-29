import requests
from bouncer.constants import *
from django.core.management.base import BaseCommand
products_url = "https://{}:{}@{}.myshopify.com/admin/products.json".format(SHOPIFY_API_KEY, SHOPIFY_PASSWORD,
                                                                           SHOP_NAME)
from bouncer.models import Product

# Collect products from shopify and dump it to the database
class Command(BaseCommand):
    def handle(self, *args, **options):
        all_products = requests.get(products_url).json()['products']
        # name, photo url, price, Link to shopify page.
        for product in all_products:
            try:
                product, created = Product.objects.get_or_create(title=product['title'],
                                                                 image_url=product['image']['src'])
                product.save()
            except (KeyError, TypeError):
                continue
