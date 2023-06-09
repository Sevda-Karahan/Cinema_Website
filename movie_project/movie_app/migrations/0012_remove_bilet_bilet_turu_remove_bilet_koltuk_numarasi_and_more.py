# Generated by Django 4.2.1 on 2023-05-18 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0010_remove_seansekle_id_alter_seansekle_seans_id')
    ]

    operations = [
        migrations.AddField(
            model_name='bilet',
            name='adet',
            field=models.IntegerField(default=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bilet',
            name='bilet_tipi',
            field=models.CharField(choices=[('tam', 'Tam Bilet'), ('ogrenci', 'Öğrenci Bilet')], default='tam', max_length=10),
        ),
        migrations.AddField(
            model_name='bilet',
            name='fiyat',
            field=models.DecimalField(decimal_places=2, default=40, max_digits=8),
            preserve_default=False,
        ),
    ]
