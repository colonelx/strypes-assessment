from django.contrib import admin
from .models.inventory import Class, Item

class InventoryClassAdmin(admin.ModelAdmin):
    pass

class InventoryItemAdmin(admin.ModelAdmin):
    pass


admin.site.register(Class, InventoryClassAdmin)
admin.site.register(Item, InventoryItemAdmin)