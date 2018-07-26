from rest_framework import serializers


class ShowItemSerializer(serializers.ModelSerializer):

    class Meta:
        from .models import Item
        model = Item
        fields = '__all__'


class AddItemSerializer(serializers.ModelSerializer):

    name = serializers.CharField(required=False)
    image = serializers.URLField(required=False)

    class Meta:
        from .models import Item

        model = Item
        fields = '__all__'


class LunchPackSerializer(serializers.ModelSerializer):

    class Meta:
        from .models import LunchPack

        model = LunchPack
        fields = '__all__'


class ShowStoreSerializer(serializers.ModelSerializer):

    class Meta:
        from .models import Store

        model = Store
        fields = '__all__'


class AddStoreSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(required=False)
    landline = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    gst_number = serializers.CharField(required=False)

    class Meta:
        from .models import Store

        model = Store
        fields = '__all__'
