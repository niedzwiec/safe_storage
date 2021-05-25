from django.contrib import admin
from safe_storage.models import Storage


# Register your models here.


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.password = hash(obj.password)
        super().save_model(request, obj, form, change)
