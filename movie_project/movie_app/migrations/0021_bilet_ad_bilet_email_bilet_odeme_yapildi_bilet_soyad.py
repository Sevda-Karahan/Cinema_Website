# Generated by Django 4.2.1 on 2023-05-19 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0020_alter_bilet_seans'),
    ]

    operations = [
        migrations.AddField(
            model_name='bilet',
            name='ad',
            field=models.CharField(default=2, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bilet',
            name='email',
            field=models.EmailField(default=5, max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bilet',
            name='odeme_yapildi',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='bilet',
            name='soyad',
            field=models.CharField(default=4, max_length=50),
            preserve_default=False,
        ),
    ]
