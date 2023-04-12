from django.db import models


class Product(models.Model):
    name = models.CharField('Название', max_length=255)
    code = models.CharField('Артикул', max_length=255, blank=True, null=True)
    price = models.DecimalField('Цена', max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
