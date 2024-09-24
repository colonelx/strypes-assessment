from django.db import models

class ActivityLog(models.Model):
    '''
    Model: ActivityLog
    '''
    '''
    IDEA: Since this needs to be a log, it is not a good idea to relate columns to other tables,
    as 
    - if we choose on_delete=CASCADE, then we will lose log records
    - if we choose on_delete=RESTRICT || PROTECT we will limit the ability to delete records.
    Therefore, I will mark all the fields as Char/Text.
    Alternatively, we can use GenericForeignKey (relationship through Django content types), but this will result in way too many columns.
    '''
    employee = models.CharField(max_length=255, null=False)
    logged_at = models.DateTimeField(null=False) 
    storage_from = models.CharField(max_length=255, null=True)
    storage_to = models.CharField(max_length=255, null=True)
    item = models.CharField(max_length=255, null=False)
    operation_type = models.CharField(max_length=255, null=False)
    coordinator = models.CharField(max_length=255, null=True)

    def __str__(self) -> str:
        return f"{self.item} {self.operation_type} by {self.employee} on {self.storage_from} -> {self.storage_to} at {self.logged_at}"