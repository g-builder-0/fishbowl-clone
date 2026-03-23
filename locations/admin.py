from django.contrib import admin
from .models import Warehouse, Location


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'city', 'state', 'is_active']
    search_fields = ['code', 'name', 'city']
    list_filter = ['is_active', 'state']   


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['code', 'warehouse', 'aisle', 'rack', 'shelf', 'is_active']
    search_fields = ['code', 'aisle']
    list_filter = ['is_active', 'warehouse']
    raw_id_fields = ['warehouse']