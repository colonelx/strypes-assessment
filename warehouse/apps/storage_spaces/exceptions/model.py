from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    from storage_spaces.models.accountables import Accountable
    from employees.models.employees import Employee

class AccountableUniqueRoleError(Exception):
    def __init__(self, obj: Accountable):
        super().__init__(
            f"There can be only one accountable with role '{obj.role.title}' in warehouse '{obj.storage_space.title}'!"
        )

class EmployeeNoPermissionError(Exception):
    def __init__(self, obj: Employee):
        super().__init__(
            f"Employee ({obj.first_name} {obj.last_name}) does not have permission 'can_manage_inventory' in order to be an Accountable!"
        )