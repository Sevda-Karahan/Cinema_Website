# Generated by Django 4.2.1 on 2023-05-07 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0004_alter_sinemaekle_options_alter_sinemaekle_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='filmekle',
            name='sinema',
            field=models.ManyToManyField(to='movie_app.sinemaekle'),
        ),
    ]