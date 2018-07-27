from django.contrib import admin
from .models import BillingHeader, BillItem


class MyModelAdmin(admin.ModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        """
        Makes created_by & create_date readonly when editing.
        """
        if not obj:
            return ()
        return 'created_by', 'create_date'

admin.site.register(BillingHeader, MyModelAdmin)
admin.site.register(BillItem)
