from django.conf import settings
from django.db import models
from base.models import BaseModel

class Product(BaseModel):
    name = models.CharField('Название', max_length=255)
    code = models.CharField('Артикул', max_length=255, blank=True, null=True)
    price = models.DecimalField('Цена', max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
