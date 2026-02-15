from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['sku', 'name', 'unit_cost', 'tracks_serial_numbers']
    search_fields = ['sku', 'name']
    list_filter = ['tracks_serial_numbers', 'tracks_lot_numbers']