# Generated by Django 4.0.4 on 2023-04-12 15:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0002_alter_orderitem_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoryOrder',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, serialize=False, verbose_name='ID')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('history_data', models.TextField()),
                ('history_all_data', models.TextField(blank=True, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'ordering': ('-history_date',),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoryOrderItem',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, serialize=False, verbose_name='ID')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('history_data', models.TextField()),
                ('history_all_data', models.TextField(blank=True, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'ordering': ('-history_date',),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.AlterField(
            model_name='order',
            name='author_create',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_author_create', to=settings.AUTH_USER_MODEL, verbose_name='Автор создания'),
        ),
        migrations.AlterField(
            model_name='order',
            name='author_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_author_update', to=settings.AUTH_USER_MODEL, verbose_name='Автор обновления'),
        ),
        migrations.AlterField(
            model_name='order',
            name='dt_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='dt_updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='author_create',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_author_create', to=settings.AUTH_USER_MODEL, verbose_name='Автор создания'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='author_update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_author_update', to=settings.AUTH_USER_MODEL, verbose_name='Автор обновления'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='dt_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='dt_updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
