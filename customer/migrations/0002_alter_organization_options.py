# Generated by Django 4.0.4 on 2023-04-12 03:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='organization',
            options={'verbose_name': 'Организация-покупатель', 'verbose_name_plural': 'Организации-покупатели'},
        ),
    ]
