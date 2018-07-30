from rest_framework import serializers


class ShowItemSerializer(serializers.ModelSerializer):
    """
    ShowItemSerializer is a model serializer to show the attributes of the item.
    """
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
    """
    LunchPackSerializer is a model serializer to show the details of the lunch pack.
    """
    class Meta:
        from .models import LunchPack

        model = LunchPack
        fields = ('id', 'name', 'price', 'items', 'category')


class ShowStoreSerializer(serializers.ModelSerializer):
    """
    ShowStoreSerializer is a model serializer to show the attributes of the store.
    """
    class Meta:
        from .models import Store

        model = Store
        fields = ('id', 'name', 'mobile', 'landline', 'address', 'gst_number')


class AddItemSerializer(serializers.ModelSerializer):
    """
    AddItemSerializer is a model serializer that includes the attributes required to add a new item.
    """
    tags = serializers.StringRelatedField(many=True)

    class Meta:
        from .models import Item

        model = Item
        fields = ('category', 'name', 'price', 'image', 'tags', 'hsn', 'desc', 'gst', 'gst_inclusive')


class ShowOrderSerializer(serializers.ModelSerializer):
    """
    ShowOrderSerializer is a model serializer that shows the attributes of an order.
    """

    class Meta:
        from .models import Order

        model = Order
        fields = ('bill', 'mode', 'address', 'payment', 'status', 'wait_time')


class UpdateFeedbackSerializer(serializers.ModelSerializer):
    """
    UpdateFeedbackSerializer is a model serializer to update the feedback of the user.
    """

    class Meta:
        from .models import Order

        model = Order
        fields = ('feedback', )
