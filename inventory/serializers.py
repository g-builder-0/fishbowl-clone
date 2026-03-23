from rest_framework import serializers
from .models import InventoryItem, InventoryTransaction


class InventoryTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryTransaction
        fields = '__all__'
        read_only_fields = ['quantity_before', 'quantity_after', 'created_at']


class InventoryItemSerializer(serializers.ModelSerializer):
    product_sku = serializers.CharField(source='product.sku', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    location_code = serializers.CharField(source='location.code', read_only=True)
    warehouse_code = serializers.CharField(source='location.warehouse.code', read_only=True)
    quantity_available = serializers.ReadOnlyField()

    class Meta:
        model = InventoryItem
        fields = '__all__'
        read_only_fields = ['quantity_on_hand', 'quantity_allocated', 'created_at', 'updated_at']