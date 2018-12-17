from django.contrib import admin

from drfaddons.admin import CreateUpdateAdmin

from .models import LeadStatus, Lead


class LeadStatusAdmin(admin.ModelAdmin):
    list_display = ('name', )


class LeadAdmin(admin.ModelAdmin):
    from comment.admin import CommentInlineAdmin

    list_display = ('name', 'status', 'created_by', 'create_date',
                    'update_date')
    list_filter = ('status', )
    inlines = (CommentInlineAdmin, )


admin.site.register(LeadStatus, LeadStatusAdmin)
admin.site.register(Lead, LeadAdmin)
