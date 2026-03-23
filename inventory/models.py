from django.db import models
from products.models import Product
from locations.models import Location


class InventoryItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='inventory_items')
    location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='inventory_items')
    quantity_on_hand = models.DecimalField(max_digits=12, decimal_places=4, default=0)
    quantity_allocated = models.DecimalField(max_digits=12, decimal_places=4, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['product', 'location']]
        ordering = ['product', 'location']

    def __str__(self):
        return f"{self.product.sku} @ {self.location} — qty: {self.quantity_on_hand}"

    @property
    def quantity_available(self):
        return self.quantity_on_hand - self.quantity_allocated


class InventoryTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('RECEIVE', 'Receive'),
        ('SHIP', 'Ship'),
        ('ADJUST', 'Adjust'),
        ('TRANSFER_IN', 'Transfer In'),
        ('TRANSFER_OUT', 'Transfer Out'),
        ('CYCLE_COUNT', 'Cycle Count'),
    ]

    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.PROTECT, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    quantity_change = models.DecimalField(max_digits=12, decimal_places=4)
    quantity_before = models.DecimalField(max_digits=12, decimal_places=4)
    quantity_after = models.DecimalField(max_digits=12, decimal_places=4)
    reference = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.transaction_type} {self.quantity_change} — {self.inventory_item}"