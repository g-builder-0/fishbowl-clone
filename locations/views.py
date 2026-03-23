from rest_framework import viewsets
from .models import Warehouse, Location
from .serializers import WarehouseSerializer, LocationSerializer


class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    lookup_field = 'code'


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.select_related('warehouse').all()
    serializer_class = LocationSerializer