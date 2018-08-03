from django.contrib import admin
from drfaddons.admin import CreateUpdateAdmin

class SocialAdmin(CreateUpdateAdmin):

    fieldsets = (
        (None, {
            'fields': ('twitter', 'instagram', 'facebook', 'date', 'verify')
        }),
        ('advanced options', {
            'classes': ('collaspe',),
            'fields': ('created_by', 'update_date')
        }),
    )
