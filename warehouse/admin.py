from django.contrib import admin

from drfaddons.admin import CreateUpdateAdmin

from .models import WarehouseManager, Warehouse, WarehouseStock, WarehouseInput


class WarehouseInputInline(admin.TabularInline):
    model = WarehouseInput
    extra = 0


class StockAdmin(CreateUpdateAdmin):
    inlines = (WarehouseInputInline, )


admin.site.register(Warehouse, CreateUpdateAdmin)
admin.site.register(WarehouseManager, CreateUpdateAdmin)
admin.site.register(WarehouseStock, StockAdmin)
