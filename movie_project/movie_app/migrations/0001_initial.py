# Generated by Django 4.2.1 on 2023-05-06 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FilmEkle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('summary', models.TextField(max_length=1000)),
                ('vision_date', models.CharField(max_length=100)),
                ('director', models.CharField(max_length=100)),
                ('actors', models.TextField(max_length=500)),
                ('formats', models.TextField(max_length=500)),
                ('date', models.DateTimeField(blank=True)),
                ('image', models.ImageField(upload_to='images/')),
                ('trailer', models.URLField(max_length=300)),
            ],
        ),
    ]
