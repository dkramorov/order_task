from django.db import models
from base.models import BaseModel, HistoryRecords
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class Order(BaseModel):
    class State(models.TextChoices):
        CREATING = ('creating', 'Создание',)
        SEND = ('send', 'Отправлен',)

    state = models.CharField('Состояние заказа', max_length=50, choices=State.choices, default=State.CREATING)
    history = HistoryRecords()

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, verbose_name='Заказ', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('catalogue.Product', verbose_name='Товар', on_delete=models.CASCADE)
    amount = models.IntegerField('Кол-во', default=0)
    history = HistoryRecords()

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказов'

    def __str__(self):
        return '#%s, Ид товара: %s, кол-во: %s' % (self.id, self.product_id, self.amount)

    def save(self, *args, **kwargs):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'test_group',
            {'type': 'chatmessage', 'message': 'Изменена позиция %s' % str(self)},
        )
        super(OrderItem, self).save(*args, **kwargs)
