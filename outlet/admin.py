from django.contrib import admin

from drfaddons.admin import CreateUpdateAdmin

from .models import Outlet, OutletImage, OutletManager, OutletProduct


class OutletProductInline(admin.StackedInline):
    model = OutletProduct
    extra = 0
    fields = ('product', 'stock')


class OutletManagerInline(admin.StackedInline):
    model = OutletManager
    extra = 0
    fields = ('manager', 'is_active')


class OutletImageInline(admin.StackedInline):
    model = OutletImage
    extra = 0
    fields = ('name', 'image')


class OutletAdmin(CreateUpdateAdmin):
    list_display = ('id', 'name', 'city', 'area', 'pincode')
    list_filter = ('city', 'area', 'pincode')
    search_fields = ('name', 'city', 'area', 'unit', 'building', 'pincode')
    inlines = (OutletManagerInline, OutletProductInline, OutletImageInline)


admin.site.register(Outlet, OutletAdmin)
