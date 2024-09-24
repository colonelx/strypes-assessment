from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from storage_spaces.models import StorageSpace
from ..exceptions.model import FreeSpaceOverflow


class Class(models.Model):
    title = models.CharField(blank=False, null=False, max_length=255)

    class Meta:
        verbose_name_plural = "classes"

    def __str__(self) -> str:
        return self.title


class Item(models.Model):
    title = models.CharField(blank=False, null=False, max_length=255)

    inventory_class = models.ForeignKey(
        Class, related_name="items", on_delete=models.CASCADE
    )
    storage_space = models.ForeignKey(
        StorageSpace, related_name="items", on_delete=models.CASCADE
    )

    # ASSUME: I am assuming a single Item represents a delivery of such object, but it may consist
    # of a package of single items ... eg. 3 cases of beer. Therefore the formula for checking against
    # storage space capacity would be Item (size * quantity) <= Storage Space available (free) space.
    size = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(xxx)x.xx In sqr. meters m^2. Single package size (eg. 1 box)",
    )
    # IDEA: I was thinking of limiting size + quantity in order to not get bigger than the storage space
    # capacity limit, but since we have a `clean()` validation check of exceeding values, for where
    # capacity counts, this is really not neccessary.
    quantity = models.IntegerField(
        default=1,
        null=True,
        blank=True,
        help_text="Quantity, for space calculation (qtty * size)",
    )
    size_total = models.GeneratedField(
        expression=models.F("quantity") * models.F("size"),
        output_field=models.DecimalField(max_digits=8, decimal_places=2),
        db_persist=False,
    )

    # IDEA: This will be implemented in the serializer validation, however I wanted to protect the
    # Models as well, from somebody using admin for istance to add Inventory.
    def clean(self):
        if self.storage_space.type.is_external == True:
            used_capacity = self.storage_space.items.exclude(id=self.pk).aggregate(
                total=models.Sum(models.F("size_total"))
            )["total"]
            used_capacity = 0 if used_capacity == None else used_capacity
            free_space = self.storage_space.capacity - used_capacity
            if (self.size * self.quantity) > free_space:
                raise FreeSpaceOverflow(self)

    def __str__(self) -> str:
        return f"{self.title} ({self.inventory_class.title})"
