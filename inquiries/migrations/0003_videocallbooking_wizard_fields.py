from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inquiries', '0002_contactsubmission_product_interest'),
    ]

    operations = [
        migrations.RenameField(
            model_name='videocallbooking',
            old_name='name',
            new_name='full_name',
        ),
        migrations.AlterField(
            model_name='videocallbooking',
            name='full_name',
            field=models.CharField(max_length=150),
        ),
        migrations.RemoveField(
            model_name='videocallbooking',
            name='notes',
        ),
        migrations.AddField(
            model_name='videocallbooking',
            name='location',
            field=models.CharField(blank=True, default='', max_length=150),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='videocallbooking',
            name='phone',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='videocallbooking',
            name='preferred_time',
            field=models.CharField(max_length=20),
        ),
        migrations.AddField(
            model_name='videocallbooking',
            name='session_key',
            field=models.CharField(blank=True, db_index=True, default='', max_length=40),
            preserve_default=False,
        ),
        migrations.RenameField(
            model_name='videocallbooking',
            old_name='submitted_at',
            new_name='created_at',
        ),
        migrations.AlterModelOptions(
            name='videocallbooking',
            options={'ordering': ['-created_at']},
        ),
    ]
