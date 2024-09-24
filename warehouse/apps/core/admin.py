from django.contrib import admin
from .models.activity_log import ActivityLog

class ActivityLogAdmin(admin.ModelAdmin):
    pass


admin.site.register(ActivityLog, ActivityLogAdmin)