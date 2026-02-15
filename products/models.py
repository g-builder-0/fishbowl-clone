from django.db import models


class Product(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    upc = models.CharField(max_length=20, blank=True)
    tracks_serial_numbers = models.BooleanField(default=False)
    tracks_lot_numbers = models.BooleanField(default=False)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sku} - {self.name}"

    class Meta:
        ordering = ['sku']
