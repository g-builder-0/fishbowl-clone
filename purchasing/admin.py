from django.contrib import admin
from .models import PurchaseOrder, PurchaseOrderLine, Receipt, ReceiptLine


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ['po_number', 'vendor_name', 'status', 'expected_date', 'created_at']
    list_filter = ['status']
    search_fields = ['po_number', 'vendor_name']


@admin.register(PurchaseOrderLine)
class PurchaseOrderLineAdmin(admin.ModelAdmin):
    list_display = ['purchase_order', 'product', 'quantity_ordered', 'quantity_received', 'unit_cost']


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ['id', 'purchase_order', 'warehouse', 'received_by', 'received_date']


@admin.register(ReceiptLine)
class ReceiptLineAdmin(admin.ModelAdmin):
    list_display = ['receipt', 'po_line', 'quantity_received', 'location']