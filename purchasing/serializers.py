from rest_framework import serializers
from .models import PurchaseOrder, PurchaseOrderLine, Receipt, ReceiptLine
from locations.models import Warehouse, Location


class PurchaseOrderLineSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = PurchaseOrderLine
        fields = ['id', 'product', 'product_name', 'quantity_ordered',
                  'quantity_received', 'unit_cost']


class PurchaseOrderSerializer(serializers.ModelSerializer):
    lines = PurchaseOrderLineSerializer(many=True)

    class Meta:
        model = PurchaseOrder
        fields = ['po_number', 'vendor_name', 'status', 'expected_date',
                  'created_at', 'lines']

    def create(self, validated_data):
        lines_data = validated_data.pop('lines')
        po = PurchaseOrder.objects.create(**validated_data)
        for line_data in lines_data:
            PurchaseOrderLine.objects.create(purchase_order=po, **line_data)
        return po


class ReceiptLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiptLine
        fields = ['po_line', 'quantity_received', 'location', 'serial_numbers']


class ReceiveInventorySerializer(serializers.Serializer):
    warehouse = serializers.PrimaryKeyRelatedField(queryset=Warehouse.objects.all())
    received_by = serializers.CharField(max_length=100)
    lines = ReceiptLineSerializer(many=True)