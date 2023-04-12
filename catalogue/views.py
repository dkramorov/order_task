
from rest_framework.viewsets import ModelViewSet
from . import models
from . import serializers


class ProductViewSet(ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
