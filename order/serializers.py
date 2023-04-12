
from rest_framework.serializers import ModelSerializer
from . import models


class OrderSerializer(ModelSerializer):

    class Meta:
        model = models.Order
        fields = ['dt_created', 'dt_updated', 'author_create', 'author_update', 'items']


class OrderItemSerializer(ModelSerializer):

    class Meta:
        model = models.OrderItem
        fields = [
            'order', 'product', 'amount', 'dt_created', 'dt_updated', 'author_create', 'author_update',
        ]
