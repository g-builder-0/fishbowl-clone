from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from .models import InventoryItem, InventoryTransaction
from .serializers import InventoryItemSerializer, InventoryTransactionSerializer
from decimal import Decimal, InvalidOperation


class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.select_related(
        'product', 'location', 'location__warehouse'
    ).all()
    serializer_class = InventoryItemSerializer

    @action(detail=True, methods=['post'])
    def adjust(self, request, pk=None):
        inventory_item = self.get_object()
        quantity_change = request.data.get('quantity_change')
        notes = request.data.get('notes', '')
        reference = request.data.get('reference', '')

        if quantity_change is None:
            return Response({'error': 'quantity_change is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            quantity_change = Decimal(str(quantity_change))
        except (ValueError, TypeError, InvalidOperation):
            return Response({'error': 'quantity_change must be a number'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            quantity_before = inventory_item.quantity_on_hand
            inventory_item.quantity_on_hand += quantity_change
            inventory_item.save()

            InventoryTransaction.objects.create(
                inventory_item=inventory_item,
                transaction_type='ADJUST',
                quantity_change=quantity_change,
                quantity_before=quantity_before,
                quantity_after=inventory_item.quantity_on_hand,
                reference=reference,
                notes=notes,
            )

        serializer = self.get_serializer(inventory_item)
        return Response(serializer.data)


class InventoryTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InventoryTransaction.objects.select_related(
        'inventory_item', 'inventory_item__product', 'inventory_item__location'
    ).all()
    serializer_class = InventoryTransactionSerializer