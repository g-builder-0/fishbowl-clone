from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from decimal import Decimal

from .models import PurchaseOrder, PurchaseOrderLine, Receipt, ReceiptLine
from .serializers import PurchaseOrderSerializer, ReceiveInventorySerializer
from inventory.models import InventoryItem, InventoryTransaction


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.prefetch_related('lines', 'lines__product').all()
    serializer_class = PurchaseOrderSerializer

    @action(detail=True, methods=['post'])
    def receive(self, request, pk=None):
        po = self.get_object()

        if po.status == 'completed':
            return Response(
                {'error': 'This PO has already been fully received'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ReceiveInventorySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated = serializer.validated_data

        with transaction.atomic():
            receipt = Receipt.objects.create(
                purchase_order=po,
                warehouse=validated['warehouse'],
                received_by=validated['received_by'],
            )

            for line_data in validated['lines']:
                po_line = line_data['po_line']
                quantity_received = line_data['quantity_received']
                location = line_data['location']

                ReceiptLine.objects.create(
                    receipt=receipt,
                    po_line=po_line,
                    quantity_received=quantity_received,
                    location=location,
                    serial_numbers=line_data.get('serial_numbers', []),
                )

                po_line.quantity_received += quantity_received
                po_line.save()

                inventory_item, _ = InventoryItem.objects.get_or_create(
                    product=po_line.product,
                    location=location,
                )
                quantity_before = inventory_item.quantity_on_hand
                inventory_item.quantity_on_hand += Decimal(str(quantity_received))
                inventory_item.save()

                InventoryTransaction.objects.create(
                    inventory_item=inventory_item,
                    transaction_type='RECEIVE',
                    quantity_change=Decimal(str(quantity_received)),
                    quantity_before=quantity_before,
                    quantity_after=inventory_item.quantity_on_hand,
                    reference=po.po_number,
                    notes=f"Received against PO {po.po_number}",
                )

            all_lines = po.lines.all()
            fully_received = all(
                line.quantity_received >= line.quantity_ordered
                for line in all_lines
            )
            po.status = 'completed' if fully_received else 'receiving'
            po.save()

        po = PurchaseOrder.objects.prefetch_related('lines', 'lines__product').get(pk=po.pk)
        return Response(PurchaseOrderSerializer(po).data)