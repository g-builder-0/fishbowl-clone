from django.contrib import admin
from .models import InventoryItem, InventoryTransaction


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'location', 'quantity_on_hand', 'quantity_allocated', 'quantity_available']
    list_filter = ['location__warehouse']
    search_fields = ['product__sku', 'product__name', 'location__code']
    raw_id_fields = ['product', 'location']
    readonly_fields = ['quantity_on_hand', 'quantity_allocated', 'created_at', 'updated_at']


@admin.register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_type', 'inventory_item', 'quantity_change', 'quantity_before', 'quantity_after', 'created_at']
    list_filter = ['transaction_type']
    search_fields = ['inventory_item__product__sku', 'reference']
    readonly_fields = ['created_at']