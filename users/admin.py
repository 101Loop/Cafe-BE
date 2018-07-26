from django.contrib import admin
from .models import *


class AuthorAdmin(admin.ModelAdmin):
    readonly_fields = ('password', )


admin.site.register(User, AuthorAdmin)
admin.site.register(OTPValidation)
admin.site.register(AuthTransaction)
