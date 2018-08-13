from django.contrib import admin
from .models import *


class PaymentRequestAdmin(admin.ModelAdmin):

    list_display = ('id', 'amount', 'purpose', 'status')
    search_fields = ('id', )
    list_filter = ('amount', 'purpose')


class PaymentAdmin(admin.ModelAdmin):

    list_display = ('id', 'status', 'currency')
    search_fields = ('id', )


admin.site.register(PaymentRequest, PaymentRequestAdmin)
admin.site.register(Payment, PaymentAdmin)
