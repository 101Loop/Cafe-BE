from rest_framework import serializers


class OutletSerializer(serializers.ModelSerializer):
    from business.serializers import PublicBusinessSerializer

    business = PublicBusinessSerializer(many=False, read_only=True)

    class Meta:
        from .models import Outlet

        model = Outlet
        fields = ('id', 'name', 'business', 'city__name', 'unit', 'building',
                  'area', 'pincode', 'city__state__name')
        read_only_fields = fields


class OutletProductSerializer(serializers.ModelSerializer):
    from product.serializers import ProductSerializer

    product = ProductSerializer(many=False, read_only=True)

    class Meta:
        from .models import OutletProduct

        model = OutletProduct
        fields = ('id', 'product', 'mrp')
