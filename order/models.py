from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Order(models.Model):
    class State(models.TextChoices):
        CREATING = ('creating', 'Создание',)
        SEND = ('send', 'Отправлен',)

    state = models.CharField('Состояние заказа', max_length=50, choices=State.choices, default=State.CREATING)
    dt_created = models.DateTimeField('Время добавления', db_index=True, auto_now_add=True)
    dt_updated = models.DateTimeField('Время обновления', db_index=True, auto_now=True)
    author_create = models.ForeignKey(
        User, verbose_name='Автор создания', on_delete=models.CASCADE,
        related_name='+',
    )
    author_update = models.ForeignKey(
        User, verbose_name='Автор обновления', on_delete=models.SET_NULL, blank=True, null=True,
        related_name='+',
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name='Заказ', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('catalogue.Product', verbose_name='Товар', on_delete=models.CASCADE)
    amount = models.IntegerField('Кол-во', default=0)
    dt_created = models.DateTimeField('Время добавления', db_index=True, auto_now_add=True)
    dt_updated = models.DateTimeField('Время обновления', db_index=True, auto_now=True)
    author_create = models.ForeignKey(
        User, verbose_name='Автор создания', on_delete=models.CASCADE,
        related_name='+',
    )
    author_update = models.ForeignKey(
        User, verbose_name='Автор обновления', on_delete=models.SET_NULL, blank=True, null=True,
        related_name='+',
    )

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказов'
