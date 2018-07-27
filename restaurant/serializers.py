from rest_framework import serializers


class ShowItemSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True)
    category = serializers.SerializerMethodField()

    class Meta:
        from .models import Item
        model = Item
        fields = ('id', 'category', 'name', 'price', 'image', 'tags', 'hsn', 'desc', 'gst', 'gst_inclusive', 'subtotal',
                  'total')

    def get_category(self, obj):
        return obj.get_category_display()


class LunchPackSerializer(serializers.ModelSerializer):

    class Meta:
        from .models import LunchPack

        model = LunchPack
        fields = ('id', 'name', 'price', 'items', 'category')


class ShowStoreSerializer(serializers.ModelSerializer):

    class Meta:
        from .models import Store

        model = Store
        fields = ('id', 'name', 'mobile', 'landline', 'address', 'gst_number')
