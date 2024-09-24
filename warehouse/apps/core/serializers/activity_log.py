from rest_framework import serializers
from ..models.activity_log import ActivityLog

class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = [
            "id",
            "coordinator",
            "employee",
            "item",
            "logged_at",
            "operation_type",
            "storage_from",
            "storage_to",
        ]