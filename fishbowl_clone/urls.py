from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from products.views import ProductViewSet
from locations.views import WarehouseViewSet, LocationViewSet
from inventory.views import InventoryItemViewSet, InventoryTransactionViewSet

router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')
router.register('warehouses', WarehouseViewSet, basename='warehouse')
router.register('locations', LocationViewSet, basename='location')
router.register('inventory', InventoryItemViewSet, basename='inventory')
router.register('transactions', InventoryTransactionViewSet, basename='transaction')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]