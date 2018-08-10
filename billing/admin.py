from django.contrib import admin
from .models import BillingHeader, BillItem
from drfaddons.admin import CreateUpdateAdmin


class MyModelAdmin(CreateUpdateAdmin):

    fieldsets = (
        ('Customer Info', {
            'fields': ('name', 'mobile', 'email')
        }),
        ('Bill Details', {
            'fields': ('bill_date', 'due_date', 'store', 'order_no', 'bill_no')
        }),
        ('advanced options', {
            'classes': ('collaspe',),
            'fields': ('created_by', 'update_date')
        }),
    )


class InstamojoAdmin(admin.ModelAdmin):

    fieldsets = (
        ('Payment Info', {
            'fields': ('amount', 'purpose', 'status', 'payment_id')
        }),
        ('advanced options', {
            'classes': ('collaspe',),
            'fields': ('allow_repeated_payments', 'redirect_url', 'payment_raw',
                       'payment_request_id', 'payment_request_raw', 'expires_at', 'bill')
        }),
    )


admin.site.register(BillingHeader, MyModelAdmin)
admin.site.register(BillItem)
