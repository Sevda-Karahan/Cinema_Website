# Generated by Django 4.2.1 on 2023-05-18 17:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0014_alter_bilet_zaman'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bilet',
            name='zaman',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 18, 17, 6, 2, 955370, tzinfo=datetime.timezone.utc)),
        ),
    ]
