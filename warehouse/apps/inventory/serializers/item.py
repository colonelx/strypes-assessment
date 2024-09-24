from rest_framework import serializers

from ..exceptions.api import APIItemSizeQttyNotProvidedError, APIStorageSpaceFreeSpaceOverflow
from ..models import Item
from storage_spaces.models import StorageSpace


class ItemSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if data["storage_space"].type.is_external:
            if ("size" not in data or "quantity" not in data) or (
                data["size"] < 1 or data["quantity"] < 1
            ):
                raise APIItemSizeQttyNotProvidedError(data["storage_space"])
            if data["size"] * data['quantity'] > data['storage_space'].free_space:
                raise APIStorageSpaceFreeSpaceOverflow(data['size'], data['quantity'], data['storage_space'])
        return data

    class Meta:
        model = Item
        fields = [
            "id",
            "title",
            "inventory_class",
            "storage_space",
            "size",
            "quantity",
            "size_total",
        ]
