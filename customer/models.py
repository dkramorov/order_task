from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser
from base.models import BaseModel


class User(AbstractUser):
    class Role(models.TextChoices):
        SHOP_ADMIN = ('shop_admin', 'Админ',)
        SHOP_STAFF = ('shop_staff', 'Сотрудник магазина',)
        ORGANIZATION_CHIEF = ('organization_chief', 'Менеджер организации',)
        ORGANIZATION_STAFF = ('organization_staff', 'Сотрудник организации',)

    organization = models.ForeignKey(
        'customer.Organization', verbose_name='Организация', on_delete=models.SET_NULL,
        related_name='users', blank=True, null=True,
    )
    role = models.CharField('Роль', max_length=255, choices=Role.choices, default=Role.SHOP_STAFF)


class Organization(BaseModel):
    name = models.CharField('Название', max_length=255)
    address = models.TextField('Адрес')
    point = models.PointField('Точка', blank=True, null=True, db_index=True)

    class Meta:
        verbose_name = 'Организация-покупатель'
        verbose_name_plural = 'Организации-покупатели'
