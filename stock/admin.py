from django.contrib import admin

from drfaddons.admin import CreateUpdateAdmin

from .models import RawMaterialMaster, UnitOfMeasurementMaster


admin.site.register(RawMaterialMaster, CreateUpdateAdmin)
admin.site.register(UnitOfMeasurementMaster, CreateUpdateAdmin)
