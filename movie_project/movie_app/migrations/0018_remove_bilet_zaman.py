# Generated by Django 4.2.1 on 2023-05-18 17:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0017_alter_bilet_zaman'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bilet',
            name='zaman',
        ),
    ]
