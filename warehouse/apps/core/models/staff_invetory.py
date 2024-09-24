from django.contrib.auth.models import Group
from django.db import models

class StaffInventory(Group):
    objects = models.Manager()
    
    class Meta:
        verbose_name_plural = "Staff Inventory"
        ordering = ['name']

    def __unicode__(self):
        return self.name