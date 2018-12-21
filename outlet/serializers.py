from rest_framework import serializers


class OutletSerializer(serializers.ModelSerializer):
    from business.serializers import PublicBusinessSerializer

    from location.serializers import CitySerializer

    business = PublicBusinessSerializer(many=False, read_only=True)
    city = CitySerializer(read_only=True)

    class Meta:
        from .models import Outlet

        model = Outlet
        fields = ('id', 'name', 'business', 'city', 'unit', 'building',
                  'area', 'pincode')
        read_only_fields = fields


class OutletProductSerializer(serializers.ModelSerializer):
    from product.serializers import CategorySerializer

    id = serializers.IntegerField(source='product.id')
    name = serializers.CharField(source='product.name')
    category = CategorySerializer(source='product.category')
    sku_code = serializers.CharField(source='product.sku_code')
    hsn = serializers.CharField(source='product.hsn')
    uom = serializers.CharField(source='product.get_uom_display')

    class Meta:
        from .models import OutletProduct

        model = OutletProduct
        fields = ('id', 'name', 'category', 'sku_code', 'hsn', 'uom', 'mrp')
