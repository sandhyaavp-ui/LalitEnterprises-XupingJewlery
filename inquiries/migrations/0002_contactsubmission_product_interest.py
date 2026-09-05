from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inquiries', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactsubmission',
            name='product_interest',
            field=models.CharField(
                max_length=20,
                choices=[('wholesale', 'Wholesale Jewellery'), ('retail', 'Retail Jewellery')],
                default='wholesale',
            ),
        ),
    ]
