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
                  'area', 'pincode', 'phone')
        read_only_fields = fields


class OutletProductSerializer(serializers.ModelSerializer):
    from product.serializers import CategorySerializer

    id = serializers.IntegerField(source='product.id')
    name = serializers.CharField(source='product.name')
    category = CategorySerializer(source='product.category')
    sku_code = serializers.CharField(source='product.sku_code')
    hsn = serializers.CharField(source='product.hsn')
    uom = serializers.CharField(source='product.uom.name')

    class Meta:
        from .models import OutletProduct

        model = OutletProduct
        fields = ('id', 'name', 'category', 'sku_code', 'hsn', 'uom', 'mrp')


class PublicOutletManagerSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='manager.name', read_only=True)
    mobile = serializers.CharField(source='manager.mobile', read_only=True)
    email = serializers.CharField(source='manager.email', read_only=True)

    class Meta:
        from .models import OutletManager

        model = OutletManager
        fields = ('name', 'mobile', 'email')
        read_only_fields = fields
