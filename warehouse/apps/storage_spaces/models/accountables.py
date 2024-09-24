from django.db import models
from .storage_space import StorageSpace
from employees.models.employees import Employee
from ..exceptions.model import AccountableUniqueRoleError, EmployeeNoPermissionError

class AccountableType(models.Model):
    title=models.CharField(blank=False, null=False, max_length=255)
    prio_idx=models.PositiveSmallIntegerField(blank=True, null=False, default=0)
    is_unique=models.BooleanField(
        blank=False, 
        null=False, 
        default=False, 
        help_text="Mark as unique if this Role has to be unique within the storage space employees.")
    
    def __str__(self):
        return self.title
    
class Accountable(models.Model):
    storage_space=models.ForeignKey(StorageSpace, related_name="accountables", on_delete=models.CASCADE)
    employee=models.ForeignKey(Employee, related_name="accountables", on_delete=models.CASCADE)
    role=models.ForeignKey(AccountableType, related_name="accountables", on_delete=models.CASCADE)

    # ASSUME: Description lacks definition for working days, therefore for
    # the sake of simplicity we will assume this person works every day in
    # the given time frame. 
    # Desired result with days of week can be achieved with:
    # - (preffered) Additional table for time schedule of employee in a given warehouse
    # - Multiple records in this table according to the day of the week and group the result in qs
    work_from=models.TimeField(auto_now=False, auto_now_add=False)
    work_until=models.TimeField(auto_now=False, auto_now_add=False)
    
    class Meta:
        # IDEA: In order to have a group 'Staff - inventory', we introduce a permission and will later check if the added
        # employee to 'Accountables' has that permission. The group management of permissions is done by the Superadmin.
        permissions = [
            ('can_manage_inventory','Can manage inventory'), 
        ]

    def clean(self):
        if self.role.is_unique == True and self.storage_space.accountables.filter(role=self.role).exclude(id=self.pk):
            raise AccountableUniqueRoleError(self)
        if self.employee.user and not self.employee.user.has_perm('can_manage_inventory'):
            raise EmployeeNoPermissionError(self.employee)

    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name} - {self.storage_space.title} - {self.role.title}"