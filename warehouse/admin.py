from django.contrib import admin

from drfaddons.admin import CreateUpdateAdmin

from .models import WarehouseManager, Warehouse


admin.site.register(Warehouse, CreateUpdateAdmin)
admin.site.register(WarehouseManager, CreateUpdateAdmin)
