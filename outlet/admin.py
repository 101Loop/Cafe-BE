from django.contrib import admin

from drfaddons.admin import CreateUpdateAdmin

from .models import Outlet, OutletImage, OutletManager


class OutletAdmin(CreateUpdateAdmin):
    list_display = ('id', 'name', 'city', 'area', 'pincode')
    list_filter = ('city', 'area', 'pincode')
    search_fields = ('name', 'city', 'area', 'unit', 'building', 'pincode')


class OutletImageAdmin(CreateUpdateAdmin):
    list_display = ('id', 'name', 'image')
    list_filter = ('outlet', )
    search_fields = ('name', )


class OutletManagerAdmin(CreateUpdateAdmin):
    list_display = ('id', 'manager', 'outlet')
    list_filter = ('manager', 'outlet')


admin.site.register(Outlet, OutletAdmin)
admin.site.register(OutletImage, OutletImageAdmin)
admin.site.register(OutletManager, OutletManagerAdmin)
