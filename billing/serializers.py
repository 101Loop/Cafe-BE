from rest_framework import serializers


class BillItemSerializer(serializers.ModelSerializer):

    class Meta:
        from .models import BillItem

        model = BillItem
        fields = '__all__'


class ShowBillingHeaderSerializer(serializers.ModelSerializer):

    class Meta:
        from .models import BillingHeader

        model = BillingHeader
        fields = '__all__'


class AddBillingHeaderSerializer(serializers.ModelSerializer):

    name = serializers.CharField(required=False)
    mobile = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)

    class Meta:
        from .models import BillingHeader

        model = BillingHeader
        fields = '__all__'
