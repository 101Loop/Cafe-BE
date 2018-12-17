from django.contrib import admin

from drfaddons.admin import CreateUpdateAdmin

from .models import Business, BusinessDocument


class BusinessDocumentInline(admin.StackedInline):
    model = BusinessDocument
    extra = 0
    readonly_fields = ("created_by", "create_date", "update_date")


class BusinessAdmin(CreateUpdateAdmin):
    list_display = ('name', 'business_type', 'pan', 'state', 'is_active')
    list_filter = ('created_by', 'business_type', 'state')
    search_fields = ('name', 'gst', 'pan', 'fssai')
    inlines = (BusinessDocumentInline, )


admin.site.register(Business, BusinessAdmin)
