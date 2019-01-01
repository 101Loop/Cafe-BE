from django.contrib import admin

from drfaddons.admin import CreateUpdateAdmin

from .models import RawMaterialMaster, UnitOfMeasurementMaster, StockCredit
from .models import RawMaterialStock


class StockCreditInline(admin.TabularInline):
    model = StockCredit
    extra = 0


class RawMaterialAdmin(CreateUpdateAdmin):
    inlines = (StockCreditInline, )


admin.site.register(RawMaterialMaster, CreateUpdateAdmin)
admin.site.register(UnitOfMeasurementMaster, CreateUpdateAdmin)
admin.site.register(RawMaterialStock, RawMaterialAdmin)
