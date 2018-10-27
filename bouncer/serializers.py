from rest_framework import serializers
from . import models

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title', 'created', 'modified', 'image_url', 'price', 'product_url', )
        model = models.Product