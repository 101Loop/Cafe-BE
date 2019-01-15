from django.contrib import admin

from drfaddons.admin import CreateUpdateAdmin

from .models import UserProfile, CategoryMaster


admin.site.register(UserProfile, CreateUpdateAdmin)
admin.site.register(CategoryMaster, CreateUpdateAdmin)
