from django.contrib import admin

from drfaddons.admin import CreateUpdateAdmin

from .models import Outlet, OutletImage, OutletManager, OutletProduct


class OutletProductInline(admin.StackedInline):
    model = OutletProduct
    extra = 0
    fields = ('product', 'stock')


class OutletManagerInline(admin.StackedInline):
    model = OutletManager
    extra = 0
    fields = ('manager', 'is_active')


class OutletImageInline(admin.StackedInline):
    model = OutletImage
    extra = 0
    fields = ('name', 'image')


class OutletProductAdmin(CreateUpdateAdmin):
    list_display = ('id', 'product_link', 'outlet_link', 'stock')
    readonly_fields = ('product_link', 'outlet_link')
    list_filter = ('product', 'outlet')

    def get_changeform_initial_data(self, request):
        from .models import Outlet

        data = {}
        if 'outlet__id' in request.GET:
            outlet = Outlet.objects.get(pk=request.GET['outlet__id'])
            data['outlet'] = outlet
        return data

    def product_link(self, obj):
        from django.urls import reverse

        from django.utils.html import format_html

        url = reverse('admin:%s_%s_change' % ('product', 'product'),
                      args=(obj.product.id,))
        return format_html('<a href="{url}">{name}</a>', url=url,
                           name=obj.product.name)
    product_link.short_description = "Product"

    def outlet_link(self, obj):
        from django.urls import reverse

        from django.utils.html import format_html

        url = reverse('admin:%s_%s_change' % ('outlet', 'outlet'),
                      args=(obj.outlet.id,))
        return format_html('<a href="{url}">{name}</a>', url=url,
                           name=obj.outlet.name)
    outlet_link.short_description = "Outlet"


class OutletAdmin(CreateUpdateAdmin):
    list_display = ('id', 'name', 'city', 'area', 'pincode', 'products')
    list_filter = ('city', 'area', 'pincode')
    search_fields = ('name', 'city', 'area', 'unit', 'building', 'pincode')
    readonly_fields = ('products', )
    inlines = (OutletManagerInline, OutletImageInline)

    def products(self, obj):
        from django.urls import reverse

        from django.utils.html import format_html

        count = obj.outletproduct_set.count()
        if count > 1:
            url = reverse("admin:outlet_outletproduct_changelist")
            url = ('<a href="{url}?outlet__id__exact={oid}">Check {op} '
                   'products</a>'
                   .format(url=url, op=count, oid=obj.id))
        elif count == 1:
            prod = obj.outletproduct_set.first()
            url = reverse("admin:outlet_outletproduct_change", args=(prod, ))
            url = '<a href="{url}">Open {prod}</a>'.format(url=url,
                                                           prod=prod.name)
        else:
            url = '0 Products <a href="{}?outlet__id={}">(Add now)</a>'.format(
                reverse("admin:outlet_outletproduct_add"), obj.id)
        return format_html(url)
    products.short_description = "Open Outlet Products"


admin.site.register(Outlet, OutletAdmin)
admin.site.register(OutletProduct, OutletProductAdmin)
admin.site.register(OutletManager)
