from rest_framework.serializers import ModelSerializer
from base.serializers import BaseSerializer
from . import models


class OrderSerializer(BaseSerializer):
    """ Изменил поведение create/update
        потому что мы отправляли идентификаторы на позицию в заказе,
        создавая заказ, но так как мы отправляли идентификаторы позиций,
        они уже были привязаны к другому заказу, я не понял эту логику,
        к тому же возникала ошибка: TypeError: Direct assignment to the reverse side of a related set is prohibited. Use items.set() instead.
        Я подменяю идентификатор заказа на новый, поэтому теперь
        этот метод перемещает позицию в новый заказ,
        можно обнулять id (item.id = None) тогда будет копирование из заказа
    """

    class Meta:
        model = models.Order
        fields = ['dt_created', 'dt_updated', 'author_create', 'author_update', 'items']

    def move_positions2new_order(self, items, order):
        prev_order = None
        for item in items:
            prev_order = item.order
            item.order = order
        order.items.set(items)

    def create(self, validated_data):
        items = validated_data.pop('items')
        order = super(OrderSerializer, self).create(validated_data)
        self.move_positions2new_order(items, order)
        return order

    def update(self, instance, validated_data):
        items = validated_data.pop('items')
        self.move_positions2new_order(items, instance)
        return super(OrderSerializer, self).update(instance, validated_data)


class OrderItemSerializer(BaseSerializer):

    class Meta:
        model = models.OrderItem
        fields = [
            'order', 'product', 'amount', 'dt_created', 'dt_updated', 'author_create', 'author_update',
        ]
