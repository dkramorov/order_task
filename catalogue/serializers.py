from rest_framework.fields import CurrentUserDefault
from rest_framework.serializers import ModelSerializer
from base.serializers import BaseSerializer
from . import models

class ProductSerializer(BaseSerializer):

    class Meta:
        model = models.Product
        fields = ['name', 'code', 'price']


