from rest_framework import serializers
from ..models import Class as InventoryClass

class InventoryClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryClass
        fields = ['id', 'title']