from django.contrib import admin
from .models import Social

class MyModelAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('twitter', 'instagram', 'facebook', 'date', 'verify')
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


admin.site.register(Social, MyModelAdmin)
