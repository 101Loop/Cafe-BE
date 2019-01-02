from django.contrib import admin

from drfaddons.admin import CreateUpdateAdmin

from .models import Employee, EmployeeDocument


admin.site.register(Employee, CreateUpdateAdmin)
admin.site.register(EmployeeDocument, CreateUpdateAdmin)
