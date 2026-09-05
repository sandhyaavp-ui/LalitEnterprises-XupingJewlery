from django.db import migrations

COLLECTIONS = [
    ('Bali', 'bali'),
    ('Stud', 'stud'),
    ('Pendant Chain', 'pendant-chain'),
    ('Chain', 'chain'),
    ('Ring', 'ring'),
    ('Kada', 'kada'),
    ('Bracelet', 'bracelet'),
    ('Adjustable Bracelet', 'adjustable-bracelet'),
]


def seed_collections(apps, schema_editor):
    Collection = apps.get_model('catalog', 'Collection')
    for name, slug in COLLECTIONS:
        Collection.objects.get_or_create(slug=slug, defaults={'name': name})


def unseed_collections(apps, schema_editor):
    Collection = apps.get_model('catalog', 'Collection')
    Collection.objects.filter(slug__in=[slug for _, slug in COLLECTIONS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_collections, unseed_collections),
    ]
