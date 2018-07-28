from django.contrib import admin
from .models import Item, Tag, LunchPack, Store, HasItem


# TODO: Show price info: subtotal, total, gst

class ItemAdmin(admin.ModelAdmin):

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
        ('Price Info', {
            'fields': ('gst', )
        }),
        ('advanced options', {
            'fields': ('created_by', 'update_date')
        }),
    )

    def get_readonly_fields(self, request, obj= None):
        """
        Makes created_by & create_date readonly when editing.
        """
        if not obj:
            return ()
        return 'created_by', 'create_date'


class LunchPackAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('name','price', 'category', 'items')
        }),
        ('advanced options', {
            'classes': ('collaspe', ),
            'fields': ('created_by', 'update_date')
        }),
    )
    def get_readonly_fields(self, request, obj=None):
        """
        Makes created_by & create_date readonly when editing.
        """
        if not obj:
            return ()
        return 'created_by', 'create_date'


class StoreAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('name', 'mobile', 'landline', 'address', 'gst_number', 'assigned_to')
        }),
        ('advanced options', {
            'classes': ('collaspe',),
            'fields': ('created_by', 'update_date')
        }),
    )
    def get_readonly_fields(self, request, obj=None):
        """
        Makes created_by & create_date readonly when editing.
        """
        if not obj:
            return ()
        return 'created_by', 'create_date'


class HasItemAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('item', 'store', 'in_stock')
        }),
        ('advanced options', {
            'classes': ('collaspe',),
            'fields': ('created_by', 'update_date')
        }),
    )
    def get_readonly_fields(self, request, obj=None):
        """
        Makes created_by & create_date readonly when editing.
        """
        if not obj:
            return ()
        return 'created_by', 'create_date'


admin.site.register(Tag)
admin.site.register(Item, ItemAdmin)
admin.site.register(LunchPack, LunchPackAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(HasItem, HasItemAdmin)
