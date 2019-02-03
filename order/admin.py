from django.contrib import admin

from drfaddons.admin import CreateUpdateAdmin

from .models import Order


class DeliveryInline(admin.TabularInline):
    from .models import Delivery

    model = Delivery
    extra = 0
    exclude = ('created_by', )


class SubOrderInline(admin.TabularInline):
    from .models import SubOrder
    model = SubOrder
    extra = 0
    exclude = ('created_by', )


class OrderAdmin(CreateUpdateAdmin):
    from transaction.admin import OrderPaymentInline

    list_display = ('id', 'outlet', 'name', 'mobile', 'status', 'total',
                    'payment_done')
    list_filter = ('status', 'delivery_type', 'outlet', 'managed_by__manager')
    readonly_fields = ('total', 'payment_done')
    inlines = (OrderPaymentInline, SubOrderInline, DeliveryInline)

    def get_changeform_initial_data(self, request):
        from outlet.models import Outlet

        data = {}
        if 'outlet__id' in request.GET:
            outlet = Outlet.objects.get(pk=request.GET['outlet__id'])
            data['outlet'] = outlet
        return data


admin.site.register(Order, OrderAdmin)
