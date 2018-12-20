from rest_framework import serializers


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import Order

        model = Order
        fields = ('id', 'name', 'mobile', 'email', 'outlet', 'status',
                  'preparation_time', )
        read_only_fields = ('status', 'preparation_time')


class SubOrderSerializer(serializers.ModelSerializer):

    order = OrderSerializer(many=False)

    def create(self, validated_data):
        order = validated_data.pop('order')
        instance = super(SubOrderSerializer, self).create(
            validated_data=validated_data)
        return instance

    class Meta:
        from .models import SubOrder

        model = SubOrder
        fields = ('id', 'order', 'item', 'quantity')
