from django.contrib import admin
from .models.storage_space import StorageSpaceType, StorageSpace
from .models.accountables import AccountableType, Accountable

class StorageSpaceTypeAdmin(admin.ModelAdmin):
    pass

class StorageSpaceAdmin(admin.ModelAdmin):
    readonly_fields=('user_space_field', 'free_space_field',)

    def user_space_field(self, obj):
        return obj.used_space

    user_space_field.short_description = 'Used Space'

    def free_space_field(self, obj):
        return obj.free_space
    
    free_space_field.short_description = 'Free Space'

class AccountableTypeAdmin(admin.ModelAdmin):
    pass

class AccountableAdmin(admin.ModelAdmin):
    pass


admin.site.register(StorageSpaceType, StorageSpaceTypeAdmin)
admin.site.register(StorageSpace, StorageSpaceAdmin)
admin.site.register(AccountableType, AccountableTypeAdmin)
admin.site.register(Accountable, AccountableAdmin)