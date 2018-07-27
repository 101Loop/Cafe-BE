from django.contrib import admin
from .models import BillingHeader, BillItem


class MyModelAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('bill_date', 'due_date', 'name', 'mobile', 'email', 'store', 'order_no', 'bill_no')
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

admin.site.register(BillingHeader, MyModelAdmin)
admin.site.register(BillItem)
