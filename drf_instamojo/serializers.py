from rest_framework import serializers


class CreatePaymentRequestSerializer(serializers.ModelSerializer):
    from billing.serializers import AddBillingHeaderSerializer

    bill = AddBillingHeaderSerializer(many=False)

    class Meta:
        from .models import PaymentRequest

        model = PaymentRequest
        fields = ('purpose', 'redirect_url', 'bill')
        read_only_fields = ('longurl', 'id')


class AndroidCreatePaymentSerializer(serializers.Serializer):
    from billing.serializers import AddBillingHeaderSerializer

    bill = AddBillingHeaderSerializer(many=False)
    payment_id = serializers.CharField(required=True)
