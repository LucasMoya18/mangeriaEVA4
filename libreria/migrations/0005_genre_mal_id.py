# Generated by Django 3.2 on 2024-12-09 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0004_alter_mangaimage_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='genre',
            name='mal_id',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
    ]
