from django.db import models
from products.models import Product
from locations.models import Warehouse, Location


class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=20, unique=True)
    vendor_name = models.CharField(max_length=100)
    status = models.CharField(
        max_length=20,
        choices=[
            ('draft', 'Draft'),
            ('submitted', 'Submitted'),
            ('receiving', 'Receiving'),
            ('completed', 'Completed'),
        ],
        default='draft'
    )
    expected_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PO-{self.po_number}"


class PurchaseOrderLine(models.Model):
    purchase_order = models.ForeignKey(
        PurchaseOrder,
        on_delete=models.CASCADE,
        related_name='lines'
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_ordered = models.IntegerField()
    quantity_received = models.IntegerField(default=0)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self): 
        return f"{self.purchase_order.po_number} - {self.product.sku}"


class Receipt(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    received_by = models.CharField(max_length=100)
    received_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Receipt {self.id} for {self.purchase_order.po_number}"


class ReceiptLine(models.Model):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, related_name='lines')
    po_line = models.ForeignKey(PurchaseOrderLine, on_delete=models.CASCADE)
    quantity_received = models.IntegerField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    serial_numbers = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"{self.receipt.id} - {self.po_line.product.sku}: {self.quantity_received}"