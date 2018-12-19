from rest_framework import serializers


class OutletSerializer(serializers.ModelSerializer):
    from business.serializers import PublicBusinessSerializer

    business = PublicBusinessSerializer(many=False, read_only=True)
    city = serializers.CharField(source='city.name', read_only=True)
    state = serializers.CharField(source='city.state.name', read_only=True)

    class Meta:
        from .models import Outlet

        model = Outlet
        fields = ('id', 'name', 'business', 'city', 'unit', 'building',
                  'area', 'pincode', 'state')
        read_only_fields = fields


class OutletProductSerializer(serializers.ModelSerializer):
    from product.serializers import ProductSerializer

    product = ProductSerializer(many=False, read_only=True)

    class Meta:
        from .models import OutletProduct

        model = OutletProduct
        fields = ('id', 'product', 'mrp')
