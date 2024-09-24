from rest_framework import serializers
from ..models import StorageSpace, StorageSpaceType, Accountable, AccountableType
from inventory.models import Item
from inventory.serializers.item import ItemSerializer
from employees.models import Employee
from datetime import datetime
from django.db.models import F, Q


class StorageSpaceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageSpaceType
        fields = ["id", "title"]


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["id", "first_name", "last_name", "job_title", "phone"]


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountableType
        fields = ["id", "title"]


class AccountablesSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(many=False, read_only=True)
    role = RoleSerializer(many=False, read_only=True)

    class Meta:
        model = Accountable
        fields = ["id", "employee", "role", "work_from", "work_until"]


class StorageSpaceSerializer(serializers.ModelSerializer):
    # TODO: Swagger and Redoc views don't exactly resolve the 'type' vs 'type_id'
    # if a type serializer is introduced, but introducing such assymetric behavior 
    # is against the idempotency of the object - GET should return whatever is sent 
    # through POST/PUT.
    #
    # What should be done is for a StorageSpaceType endpoint to be introduced, which
    # is outseide of scope for this task.
    #
    # Other workaround is of course introducing both fields 'type' and 'type_id' to the
    # field list
    items = ItemSerializer(many=True, read_only=True)
    currently_working_employees = serializers.SerializerMethodField()
    employees = AccountablesSerializer(source="accountables", many=True, read_only=True)

    class Meta:
        model = StorageSpace
        fields = [
            "id",
            "title",
            "type",
            "priority",
            "capacity",
            "used_space",
            "free_space",
            "has_inventory",
            "items",
            "employees",
            "currently_working_employees",
        ]
        read_only_fields = [
            "used_space",
            "free_space",
            "has_inventory",
            "items",
            "employees",
        ]

    def get_currently_working_employees(self, obj):
        timenow = str(datetime.now().time())

        # IDEA: Since the time schedule is not based on real calendar days, we need to take into account
        # the reversed ranges (eg. start: 22:00 / end: 06:00 on the next day, aka 'night shifts').
        accountables = (
            Accountable.objects.filter(id__in=obj.accountables.all())
            .filter(
                Q(
                    Q(work_from__gt=F("work_until"))
                    & (Q(work_until__gte=timenow) | Q(work_from__lte=timenow))
                )
                | Q(work_from__lte=timenow, work_until__gte=timenow)
            )
            .order_by("role__prio_idx")
        )

        return AccountablesSerializer(accountables.all(), many=True).data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["used_space"] = (
            "N/A"
            if representation["used_space"] == -1
            else representation["used_space"]
        )
        representation["free_space"] = (
            "N/A"
            if representation["free_space"] == -1
            else representation["free_space"]
        )
        return representation
