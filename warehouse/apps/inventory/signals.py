from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from .models import Item
from storage_spaces.models import STORAGE_SPACE_PRIO_RAISED, STORAGE_SPACE_PRIO_HIGH, StorageSpace
from core.models.activity_log import ActivityLog
from core.local import get_current_user
from employees.models import Employee
from datetime import datetime

PRIORITIES_TO_NOTIFY = [STORAGE_SPACE_PRIO_RAISED, STORAGE_SPACE_PRIO_HIGH]
OPERATION_TYPE_INSERT = "Insert"
OPERATION_TYPE_MOVE = "Move"
OPERATION_TYPE_DELETE = "Delete"

"""
IDEA: It is preffered this signal to be registered to the Model it corresponds to,
however we might be breaking the 'Single Responsibility' principle out of SOLID, plus
the Django documentation actually recommends for Signals to be defined separately.
"""


@receiver(pre_save, sender=Item)
def log_notify_stock_changed(sender, instance: Item, *args, **kwargs):
    old_instance = Item.objects.filter(pk=instance.pk).first()
    if not old_instance or (
        instance.storage_space_id != old_instance.storage_space_id
        and (
            instance.storage_space.priority in PRIORITIES_TO_NOTIFY
            or old_instance.storage_space.priority in PRIORITIES_TO_NOTIFY
        )
    ):
        user = get_current_user()
        # IDEA: In order to fetch the current user, we must introduce a middleware to store the user
        # that made the request in a thread-local storage.
        employee = Employee.objects.get(user=user)
        storage_from = old_instance.storage_space if old_instance else None
        operation_type = (
            OPERATION_TYPE_INSERT if old_instance is None else OPERATION_TYPE_MOVE
        )
        coordinator_name = _get_coordinator_names_by_storage(instance.storage_space)
        log_entry = ActivityLog(
            employee=f"{employee.first_name} {employee.last_name} ({employee.phone})",
            logged_at=datetime.now(),
            storage_from=storage_from.title if storage_from is not None else None,
            storage_to=instance.storage_space.title,
            item=instance.title,
            operation_type=operation_type,
            coordinator=coordinator_name,
        ).save()


@receiver(pre_delete, sender=Item)
def log_notify_stock_deleted(sender, instance: Item, *args, **kwargs):
    user = get_current_user()
    employee = Employee.objects.get(user=user)
    coordinator_name = _get_coordinator_names_by_storage(instance.storage_space)
    log_entry = ActivityLog(
        employee=f"{employee.first_name} {employee.last_name} ({employee.phone})",
        logged_at=datetime.now,
        storage_from=instance.storage_space.title,
        storage_to=None,
        item=instance.title,
        operation_type=OPERATION_TYPE_DELETE,
        coordinator=coordinator_name,
    ).save()

def _get_coordinator_names_by_storage(storage_space: StorageSpace):
    coordinator = storage_space.accountables.filter(
        role__is_unique=True
    ).first()
    coordinator_names = None
    if coordinator:
        coordinator_names = (
            f"{coordinator.employee.first_name} {coordinator.employee.last_name}"
        )
    return coordinator_names