from rest_framework import serializers


class OrderPaymentSerializer(serializers.ModelSerializer):
    order_url = serializers.HyperlinkedRelatedField(
        source='order_id', many=False, read_only=True,
        view_name='order:order-retrieve', lookup_field='pk'
    )

    def validate(self, attrs):
        if not self.instance:
            attrs['created_by'] = attrs.get('order').created_by
        return attrs

    class Meta:
        from .models import OrderPayment

        model = OrderPayment
        fields = ('id', 'order', 'amount', 'is_credit', 'payment_type',
                  'payment_mode', 'accepted_by', 'created_by', 'order_url')
        read_only_fields = ('accepted_by', 'created_by', 'order_url')
