from decimal import Decimal
from django.db import migrations

PRODUCTS = [
    ('bali', 'Classic Gold Bali', 'BALI-001', '450.00'),
    ('bali', 'Classic Gold Bali', 'BALI-002', '480.00'),
    ('stud', 'Everyday Stud', 'STUD-001', '220.00'),
    ('stud', 'Everyday Stud', 'STUD-002', '240.00'),
    ('pendant-chain', 'Pendant Chain', 'PNDC-001', '650.00'),
    ('chain', 'Everyday Chain', 'CHN-001', '520.00'),
    ('ring', 'Adjustable Ring', 'RING-001', '180.00'),
    ('kada', 'Classic Kada', 'KADA-001', '850.00'),
    ('bracelet', 'Everyday Bracelet', 'BRC-001', '390.00'),
    ('adjustable-bracelet', 'Adjustable Bracelet', 'ABRC-001', '410.00'),
]


def seed_products(apps, schema_editor):
    Collection = apps.get_model('catalog', 'Collection')
    Product = apps.get_model('catalog', 'Product')
    for slug, name, sku, price in PRODUCTS:
        try:
            collection = Collection.objects.get(slug=slug)
        except Collection.DoesNotExist:
            continue
        Product.objects.get_or_create(
            sku=sku,
            defaults={
                'name': name,
                'collection': collection,
                'price': Decimal(price),
                'moq': 6,
                'in_stock': True,
                'description': 'Placeholder product — update with real details via the admin panel.',
            },
        )


def unseed_products(apps, schema_editor):
    Product = apps.get_model('catalog', 'Product')
    Product.objects.filter(sku__in=[sku for _, _, sku, _ in PRODUCTS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_seed_collections'),
    ]

    operations = [
        migrations.RunPython(seed_products, unseed_products),
    ]
