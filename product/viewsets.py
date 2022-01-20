from rest_framework import viewsets
from . import models
from . import serializers

class ProductaddView(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductDetailsSerializer
