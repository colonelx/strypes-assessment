from django.db import models

STORAGE_SPACE_PRIO_LOW='L'
STORAGE_SPACE_PRIO_STANDARD='S'
STORAGE_SPACE_PRIO_RAISED='R'
STORAGE_SPACE_PRIO_HIGH='H'
STORAGE_SPACE_PRIOS = {
    STORAGE_SPACE_PRIO_LOW: 'Low',
    STORAGE_SPACE_PRIO_STANDARD: 'Standard',
    STORAGE_SPACE_PRIO_RAISED: 'Raised',
    STORAGE_SPACE_PRIO_HIGH: 'High',
}

class StorageSpaceType(models.Model):
    title=models.CharField(blank=False, null=False, max_length=255)

    # ASSUME: Assuming more than one type could be marked as 'external',
    # otherways we can just mark a single record as 'unique=True' for is_external.
    is_external=models.BooleanField(blank=False, null=False, default=False)

    def __str__(self) -> str:
       return self.title if self.is_external == False else f"{self.title} (external)"

class StorageSpace(models.Model):
    title=models.CharField(blank=False, null=False, max_length=255)
    
    type=models.ForeignKey(StorageSpaceType, related_name="storage_spaces", on_delete=models.CASCADE)

    priority=models.CharField(
        max_length=2,
        choices=STORAGE_SPACE_PRIOS,
        # ASSUME: No default prio mentioned, so assuming 'Low', otherwise
        # column could be marked as 'required'
        default=STORAGE_SPACE_PRIO_LOW
    )

    # ASSUME: capacity is total capacity of the storage space formated (and limited to) xxxxxx.xx. 
    # This mainly concerns the field limit (max_digits).
    capacity=models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        null=True, 
        help_text="(xxxxx)x.xx In sqr. meters m^2"
    )

    @property
    def used_space(self):
        if self.type.is_external == True:
            used = self.items.aggregate(total=models.Sum(models.F('size_total')))['total']
            return used if used is not None else 0
        return -1
    
    @property
    def free_space(self):
        if self.type.is_external == True:
            return self.capacity - self.used_space
        return -1
    
    @property
    def has_inventory(self):
        return self.items.count() > 0

    def __str__(self) -> str:
        return f"{self.title} ({self.type.title})"
    