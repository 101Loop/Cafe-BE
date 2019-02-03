from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        from .models import Category

        model = Category
        fields = ('id', 'name', 'hsn', 'create_date', 'update_date')
        read_only_fields = fields


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False, read_only=True)

    class Meta:
        from .models import Product

        model = Product
        fields = ('id', 'name', 'category', 'sku_code', 'hsn', 'uom__name',
                  'create_date', 'update_date')
        read_only_fields = fields
