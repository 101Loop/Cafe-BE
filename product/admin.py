from django.contrib import admin

from drfaddons.admin import CreateUpdateAdmin

from .models import Product, Category, ProductImage


class ProductImageAdminInline(admin.StackedInline):
    model = ProductImage
    extra = 0
    exclude = ('created_by', 'create_date', 'update_date')


class CategoryAdmin(CreateUpdateAdmin):
    list_display = ('name', 'hsn', 'sku_prefix')
    search_fields = list_display


class ProductAdmin(CreateUpdateAdmin):
    list_display = ('name', 'category', 'price', 'hsn', 'sku_code')
    search_fields = ('name', )
    list_filter = ('category', )
    inlines = (ProductImageAdminInline, )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
