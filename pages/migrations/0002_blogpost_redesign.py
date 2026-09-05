from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='cover_image',
        ),
        migrations.AddField(
            model_name='blogpost',
            name='excerpt',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='blogpost',
            name='read_minutes',
            field=models.PositiveIntegerField(default=5),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='body',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='published_at',
            field=models.DateField(),
        ),
    ]
