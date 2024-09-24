from __future__ import annotations
import typing

if typing.TYPE_CHECKING:
    from storage_spaces.models import StorageSpace


class APIItemSizeQttyNotProvidedError(Exception):
    def __init__(self, storage_space: StorageSpace):
        super().__init__(
            f"Qtty and Size are required for storage space '{storage_space.title}'"
        )


class APIStorageSpaceFreeSpaceOverflow(Exception):
    def __init__(self, size: float, quantity: int, storage_space: StorageSpace):
        super().__init__(
            f"Qtty too big '{(size * quantity)}' for available free space '{storage_space.free_space}' in storage space '{storage_space.title}'"
        )
