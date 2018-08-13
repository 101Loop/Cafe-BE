from rest_framework import serializers


class ShowBillItemSerializer(serializers.ModelSerializer):
    from restaurant.serializers import ShowItemSerializer

    item = ShowItemSerializer(many=False)

    class Meta:
        from .models import BillItem

        model = BillItem
        fields = ('id', 'item', 'quantity')


class ShowBillSerializer(serializers.ModelSerializer):
    from restaurant.serializers import ShowStoreSerializer

    store = ShowStoreSerializer(many=False)
    billitem_set = ShowBillItemSerializer(many=True)

    class Meta:
        from .models import BillingHeader

        model = BillingHeader
        fields = ('id', 'bill_date', 'due_date', 'name', 'mobile', 'email', 'store', 'subtotal', 'total', 'gst',
                  'billitem_set', 'create_date', 'created_by', 'paid', 'payment_mode', 'order_mode', 'address',
                  'payment_id')


class AddBillItemSerializer(serializers.ModelSerializer):

    class Meta:
        from .models import BillItem

        model = BillItem
        fields = ('item', 'quantity')


class AddBillingHeaderSerializer(serializers.ModelSerializer):
    """
    AddBillingHeaderSerializer is a model serializer that includes the attributes required for creating a new bill.
    """
    billitem_set = AddBillItemSerializer(many=True)

    class Meta:
        from .models import BillingHeader

        model = BillingHeader
        fields = ('id', 'bill_date', 'due_date', 'name', 'mobile', 'email', 'store', 'billitem_set', 'paid',
                  'payment_mode', 'order_mode', 'address')

    def create(self, validated_data):
        from .models import BillingHeader, BillItem

        items = validated_data.pop('billitem_set')
        bh = BillingHeader.objects.create(**validated_data)
        for item in items:
            BillItem.objects.create(billheader=bh, **item)
        return bh
