from django.contrib import admin
from .models import BillingHeader, BillItem
from drfaddons.admin import CreateUpdateAdmin


class MyModelAdmin(CreateUpdateAdmin):

    fieldsets = (
        ('Customer Info', {
            'fields': ('name', 'mobile', 'email', 'address')
        }),
        ('Bill Details', {
            'fields': ('bill_date', 'due_date', 'store', 'payment_mode', 'paid', 'order_mode')
        }),
        ('advanced options', {
            'classes': ('collapse',),
            'fields': ('created_by', 'update_date')
        }),
    )


admin.site.register(BillingHeader, MyModelAdmin)
admin.site.register(BillItem)
