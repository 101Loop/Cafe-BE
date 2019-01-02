from rest_framework import serializers

from django.utils.text import gettext_lazy as _


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        from .models import Delivery

        model = Delivery
        fields = ('id', 'amount', 'area', 'build', 'unit_no', 'address_line2',
                  'full_address')
        read_only_fields = ('full_address', )


class SubOrderSerializer(serializers.ModelSerializer):
    from outlet.serializers import OutletProductSerializer

    product = OutletProductSerializer(many=False, read_only=True)

    class Meta:
        from .models import SubOrder

        model = SubOrder
        fields = ('id', 'item', 'product', 'quantity', 'sub_total')
        read_only_fields = ('product', 'sub_total')
        extra_kwargs = {
            "item": {"write_only": True}
        }


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for placing an order

    Author: Himanshu Shankar (https://himanshus.com)
    """

    from outlet.serializers import PublicOutletManagerSerializer
    from outlet.models import Outlet

    suborder_set = SubOrderSerializer(many=True)
    status = serializers.CharField(source='get_status_display', read_only=True)
    managed_by = PublicOutletManagerSerializer(read_only=True, many=False)
    outlet_id = serializers.PrimaryKeyRelatedField(
        source='outlet', queryset=Outlet.objects.all(), write_only=True)
    outlet = serializers.HyperlinkedRelatedField(
        many=False, read_only=True, view_name='outlet:outlet-detail',
        lookup_field='pk')
    delivery = DeliverySerializer(many=False, default=None)

    def validate_suborder_set(self, value):
        if len(value) is 0:
            raise serializers.ValidationError(_("Minimum 1 item required to "
                                                "place an order."))
        return value

    def validate(self, attrs):
        from OfficeCafe.variables import DELIVERED

        if not self.instance:
            user = self.context.get('request').user
            for key in ['name', 'email', 'mobile']:
                if key not in attrs.keys():
                    attrs[key] = getattr(user, key)

            if ('delivery_type' in attrs
                    and attrs.get('delivery_type') == DELIVERED):
                if 'delivery' not in attrs or not attrs.get('delivery'):
                    raise serializers.ValidationError(
                        _("Please provide delivery address."))
                else:
                    if (attrs.get('delivery').get('area') not in
                            attrs.get('outlet').serviceable_area.all()):
                        raise serializers.ValidationError(
                            _("This outlet currently doesn't deliver in "
                              "provided area."))

        return attrs

    def create(self, validated_data):
        from .models import SubOrder, Delivery

        suborder_set = validated_data.pop('suborder_set')
        try:
            delivery = validated_data.pop('delivery')
        except KeyError:
            delivery = None

        instance = super(OrderSerializer, self).create(
            validated_data=validated_data)
        for so in suborder_set:
            SubOrder.objects.create(order=instance,
                                    created_by=instance.created_by,
                                    **so)
        if delivery:
            Delivery.objects.create(created_by=instance.created_by,
                                    order=instance,
                                    **delivery)
        return instance

    class Meta:
        from .models import Order

        model = Order
        fields = ('id', 'name', 'mobile', 'email', 'status', 'outlet_id',
                  'preparation_time', 'suborder_set', 'total', 'outlet',
                  'managed_by', 'create_date', 'update_date', 'delivery_type',
                  'payment_done', 'delivery')
        read_only_fields = ('status', 'preparation_time', 'total',
                            'create_date', 'update_date', 'payment_done')


class OrderListSerializer(serializers.ModelSerializer):
    outlet = serializers.HyperlinkedRelatedField(
        many=False, read_only=True, view_name='outlet:outlet-detail',
        lookup_field='pk')
    detail = serializers.HyperlinkedRelatedField(
        source='id', many=False, read_only=True,
        view_name='order:order-retrieve', lookup_field='pk')

    update = serializers.HyperlinkedRelatedField(
        source='id', many=False, read_only=True,
        view_name='order:order-update', lookup_field='pk')

    status_display = serializers.CharField(source='get_status_display')

    phone = serializers.CharField(source='outlet.phone', read_only=True)

    class Meta:
        from .models import Order

        model = Order
        fields = ('id', 'name', 'mobile', 'email', 'status', 'create_date',
                  'preparation_time', 'total', 'outlet', 'managed_by',
                  'status_display', 'update_date', 'phone', 'detail', 'update'
                  'delivery_type', 'payment_done')
        read_only_fields = fields


class OrderUpdateSerializer(serializers.ModelSerializer):
    from outlet.serializers import PublicOutletManagerSerializer

    suborder_set = SubOrderSerializer(many=True)
    managed_by = PublicOutletManagerSerializer(read_only=True, many=False)
    outlet = serializers.HyperlinkedRelatedField(
        many=False, read_only=True, view_name='outlet:outlet-detail',
        lookup_field='pk')
    delivery = DeliverySerializer(many=False)

    def update(self, instance, validated_data):
        from django.utils import timezone

        if 'preparation_time' in validated_data:
            preparation_time = validated_data.pop('preparation_time')
            now = timezone.now()
            etd = now + preparation_time
            preparation_time = etd - instance.create_date
            validated_data['preparation_time'] = preparation_time

        return super(OrderUpdateSerializer, self).update(
            instance=instance, validated_data=validated_data)

    class Meta:
        from .models import Order

        model = Order
        fields = ('id', 'name', 'mobile', 'email', 'status',
                  'preparation_time', 'suborder_set', 'total', 'outlet',
                  'managed_by', 'create_date', 'update_date', 'delivery_type',
                  'payment_done', 'delivery')
        read_only_fields = ('id', 'name', 'mobile', 'email', 'suborder_set',
                            'total', 'outlet', 'managed_by', 'delivery_type',
                            'payment_done', 'delivery')
