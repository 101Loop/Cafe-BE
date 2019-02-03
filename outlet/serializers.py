from rest_framework import serializers


class OutletSerializer(serializers.ModelSerializer):
    from business.serializers import PublicBusinessSerializer

    from location.serializers import AreaSerializer

    business = PublicBusinessSerializer(many=False, read_only=True)
    area = AreaSerializer(read_only=True)

    class Meta:
        from .models import Outlet

        model = Outlet
        fields = ('id', 'name', 'business', 'unit', 'building',
                  'area', 'pincode', 'phone', 'full_address')
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


class ManagerOutletStockSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import OutletStock

        model = OutletStock
        fields = ('id', 'raw_material', 'quantity', 'create_date',
                  'update_date', 'created_by')
        read_only_fields = ('create_date', 'update_date', 'created_by')


class ManagerOutletProcurementSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import OutletProcurement

        model = OutletProcurement
        fields = ('id', 'stock', 'quantity', 'date', 'mfg_date', 'exp_date',
                  'mfg_batch', 'other', 'created_by', 'create_date',
                  'update_date')
        read_only_fields = ('created_by', 'create_date', 'update_date')


class ManagerOutletStockRequestSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import OutletStockRequest

        model = OutletStockRequest
        fields = ('id', 'batch_id', 'stock', 'quantity', 'fulfilled_on',
                  'created_by', 'create_date', 'update_date')
        read_only_fields = ('batch_id', 'created_by', 'create_date',
                            'update_date')
