# Generated by Django 4.2.1 on 2023-05-06 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filmekle',
            name='image',
            field=models.URLField(max_length=500),
        ),
    ]
