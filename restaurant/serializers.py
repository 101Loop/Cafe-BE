from rest_framework import serializers


class ShowItemSerializer(serializers.ModelSerializer):
    """
    ShowItemSerializer is a model serializer to show the attributes of the item.
    """
    tags = serializers.StringRelatedField(many=True)
    category = serializers.SerializerMethodField()
    price = serializers.DecimalField(decimal_places=2, max_digits=10)

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
    Returns
    -------
        returns a dictionary containing::
            'id' : int
            'name' : str
            'price' : decimal
            'items' : str
            'category' : str
    """
    class Meta:
        from .models import LunchPack

        model = LunchPack
        fields = ('id', 'name', 'price', 'items', 'category')


class ShowStoreSerializer(serializers.ModelSerializer):
    """
    ShowStoreSerializer is a model serializer to show the attributes of the store.
    Returns
    -------
        returns a dictionary containing::
            'id' : int
            'name' : str
            'mobile' : str
            'landline' : str
            'address' : str
            'gst_number' : str
    """
    class Meta:
        from .models import Store

        model = Store
        fields = ('id', 'name', 'mobile', 'landline', 'address', 'gst_number')


class AddItemSerializer(serializers.ModelSerializer):
    """
    AddItemSerializer is a model serializer that includes the attributes required to add a new item.
    Returns
    -------
        returns a dictionary containing::
            'category' : str
            'name' : str
            'price' : decimal
            'image' : str
            'tags' : str
            'hsn' : str
            'desc' : str
            'gst' : decimal
            'gst_inclusive' : bool
    """
    tags = serializers.StringRelatedField(many=True)

    class Meta:
        from .models import Item

        model = Item
        fields = ('category', 'name', 'price', 'image', 'tags', 'hsn', 'desc', 'gst', 'gst_inclusive')


class ShowOrderSerializer(serializers.ModelSerializer):
    """
    ShowOrderSerializer is a model serializer that shows the attributes of an order.
    Returns
    -------
        returns a dictionary containing::
            'bill' : str
            'mode' : float
            'address' : str
            'payment' : str
            'status' : str
            'wait_time' : str
    """
    from billing.serializers import ShowBillSerializer

    bill = ShowBillSerializer(many=False)

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


class ShowTagSerializer(serializers.ModelSerializer):

    class Meta:
        from .models import Tag

        model = Tag
        fields = ('tag', )
