from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate_sku(self, value):
        """Convert SKU to uppercase"""
        return value.upper()