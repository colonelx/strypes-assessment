from rest_framework import permissions, viewsets
from .models import Item, Class as InventoryClass
from .serializers.inventory_class import InventoryClassSerializer
from .serializers.item import ItemSerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated]

class ClassViewSet(viewsets.ModelViewSet):
    queryset = InventoryClass.objects.all()
    serializer_class = InventoryClassSerializer
    permission_classes = [permissions.IsAuthenticated]