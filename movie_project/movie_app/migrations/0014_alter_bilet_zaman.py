# Generated by Django 4.2.1 on 2023-05-18 17:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0013_remove_bilet_adet_remove_bilet_bilet_tipi_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bilet',
            name='zaman',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
