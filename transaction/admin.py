from django.contrib import admin

from .models import OrderPayment


class OrderPaymentInline(admin.TabularInline):
    model = OrderPayment
    extra = 0
    exclude = ('created_by', )
