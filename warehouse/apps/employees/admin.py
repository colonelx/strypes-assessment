from django.contrib import admin
from .models.employees import Employee

class EmployeeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Employee, EmployeeAdmin)