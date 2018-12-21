from rest_framework import serializers

from django.utils.text import gettext_lazy as _


class SubOrderSerializer(serializers.ModelSerializer):
    from product.serializers import ProductSerializer

    product = ProductSerializer(many=False, read_only=True)

    class Meta:
        from .models import SubOrder

        model = SubOrder
        fields = ('id', 'item', 'product', 'quantity', 'sub_total')
        read_only_fields = ('product', 'sub_total')


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for placing an order

    Author: Himanshu Shankar (https://himanshus.com)
    """

    suborder_set = SubOrderSerializer(many=True)

    def validate_suborder_set(self, value):
        if len(value) is 0:
            raise serializers.ValidationError(_("Minimum 1 item required to "
                                                "place an order."))
        return value

    def validate(self, attrs):
        if not self.instance:
            user = self.context.get('request').user
            for key in ['name', 'email', 'mobile']:
                if key not in attrs.keys():
                    attrs[key] = getattr(user, key)
        return attrs

    def create(self, validated_data):
        from .models import SubOrder

        suborder_set = validated_data.pop('suborder_set')
        instance = super(OrderSerializer, self).create(
            validated_data=validated_data)
        for so in suborder_set:
            SubOrder.objects.create(order=instance,
                                    created_by=instance.created_by,
                                    **so)
        return instance

    class Meta:
        from .models import Order

        model = Order
        fields = ('id', 'name', 'mobile', 'email', 'outlet', 'status',
                  'preparation_time', 'suborder_set', 'total')
        read_only_fields = ('status', 'preparation_time', 'total')
