from django.contrib import admin
from .models import *
from drfaddons.admin import CreateUpdateAdmin


# TODO: Show price info: subtotal, total, gst

class ItemAdmin(CreateUpdateAdmin):

    list_display = ('name', 'category', 'price')
    search_fields = ('name', 'tags', 'category')
    list_filter = ('tags', 'category')
    readonly_fields = ('subtotal', 'total')
    fieldsets = (
        ('Main Section', {
            'fields': ('name', 'price', 'image', 'desc')
        }),
        ('Taggings', {
            'fields': ('category', 'tags')
        }),
        ('Good and Service Tax Information', {
            'fields': ('hsn', 'gst', 'gst_inclusive')
        }),
        ('advanced options', {
            'classes': ('collaspe',),
            'fields': ('created_by', 'update_date')
        }),
    )


class LunchPackAdmin(CreateUpdateAdmin):

    fieldsets = (
        (None, {
            'fields': ('name', 'price', 'category', 'items')
        }),
        ('advanced options', {
            'classes': ('collaspe', ),
            'fields': ('created_by', 'update_date')
        }),
    )


class StoreAdmin(CreateUpdateAdmin):

    fieldsets = (
        (None, {
            'fields': ('name', 'mobile', 'landline', 'address', 'gst_number', 'assigned_to')
        }),
        ('advanced options', {
            'classes': ('collaspe',),
            'fields': ('created_by', 'update_date')
        }),
    )


class HasItemAdmin(CreateUpdateAdmin):

    fieldsets = (
        (None, {
            'fields': ('item', 'store', 'in_stock')
        }),
        ('advanced options', {
            'classes': ('collaspe',),
            'fields': ('created_by', 'update_date')
        }),
    )


admin.site.register(Tag)
admin.site.register(Item, ItemAdmin)
admin.site.register(LunchPack, LunchPackAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(HasItem, HasItemAdmin)
admin.site.register(Cook)
