from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        from .models import Category

        model = Category
        fields = ('id', 'name', 'hsn')
        read_only_fields = fields


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import Product

        model = Product
        fields = ('id', 'name', 'category', 'sku_code', 'hsn', 'uom',
                  'is_combo', 'combo_product')
        read_only_fields = fields
