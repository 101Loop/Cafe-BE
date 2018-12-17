from django.contrib import admin

from drfaddons.admin import CreateUpdateAdmin

from .models import Tax


class TaxAdmin(CreateUpdateAdmin):
    list_display = ('name', 'display_name', 'percentage')
    search_fields = list_display


admin.site.register(Tax, TaxAdmin)
