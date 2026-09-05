from django.db import migrations, models
from django.utils.text import slugify


def backfill_slugs(apps, schema_editor):
    Product = apps.get_model('catalog', 'Product')
    for product in Product.objects.all():
        base_slug = slugify(product.name)
        slug = base_slug
        i = 1
        while Product.objects.filter(slug=slug).exclude(pk=product.pk).exists():
            i += 1
            slug = f"{base_slug}-{i}"
        product.slug = slug
        product.save(update_fields=['slug'])


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_remove_product_price_remove_product_sku'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='in_stock',
        ),
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(max_length=220, unique=True, null=True, blank=True),
        ),
        migrations.RunPython(backfill_slugs, noop),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(max_length=220, unique=True, blank=True),
        ),
    ]
