from django.contrib import admin
from .models import *
from drfaddons.admin import CreateUpdateAdmin


class ItemAdmin(CreateUpdateAdmin):

    list_display = ('name', 'category', 'total')
    search_fields = ('name', 'tags', 'category')
    list_filter = ('tags', 'category')
    readonly_fields = ()

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return super().get_readonly_fields(request, obj) + ('subtotal', 'total')
        return super().get_readonly_fields(request, obj)

    def get_fieldsets(self, request, obj=None):
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
                'classes': ('collapse',),
                'fields': ('created_by', 'update_date')
            }),
        )

        if obj:
            fieldsets[2][1]['fields'] += ('subtotal', 'total')
            return fieldsets
        return fieldsets


class LunchPackAdmin(CreateUpdateAdmin):

    fieldsets = (
        (None, {
            'fields': ('name', 'price', 'category', 'items')
        }),
        ('advanced options', {
            'classes': ('collapse', ),
            'fields': ('created_by', 'update_date')
        }),
    )


class StoreAdmin(CreateUpdateAdmin):

    fieldsets = (
        (None, {
            'fields': ('name', 'mobile', 'landline', 'address', 'gst_number', 'assigned_to')
        }),
        ('advanced options', {
            'classes': ('collapse',),
            'fields': ('created_by', 'update_date')
        }),
    )


class HasItemAdmin(CreateUpdateAdmin):

    fieldsets = (
        (None, {
            'fields': ('item', 'store', 'in_stock')
        }),
        ('advanced options', {
            'classes': ('collapse',),
            'fields': ('created_by', 'update_date')
        }),
    )


admin.site.register(Tag)
admin.site.register(Item, ItemAdmin)
admin.site.register(LunchPack, LunchPackAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(HasItem, HasItemAdmin)
admin.site.register(Cook)
