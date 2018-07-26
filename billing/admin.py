from django.contrib import admin
from .models import BillingHeader, BillItem

admin.site.register(BillingHeader)
admin.site.register(BillItem)
