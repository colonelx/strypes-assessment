from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    from inventory.models.inventory import Item

class FreeSpaceOverflow(Exception):
    def __init__(self, obj: Item):
        super().__init__(
            f"Qtty too big '{(obj.size * obj.quantity)}' for available free space '{obj.storage_space.free_space}' in warehouse '{obj.storage_space.title}'"
        )