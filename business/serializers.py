from rest_framework import serializers


class PublicBusinessSerializer(serializers.ModelSerializer):
    from location.serializers import StateSerializer

    state = StateSerializer(many=False)

    class Meta:
        from .models import Business

        model = Business
        fields = ('id', 'name', 'gst', 'pan', 'state', 'fssai', 'legal_name')


class BusinessSerializer(serializers.ModelSerializer):
    from drf_user.serializers import UserShowSerializer

    owners = UserShowSerializer(many=True, read_only=True)
    managers = UserShowSerializer(many=True, read_only=True)

    class Meta:
        from .models import Business

        model = Business
        fields = ('id', 'name', 'business_type', 'owners', 'managers',
                  'gst', 'pan', 'state', 'fssai', 'is_active', 'legal_name')
        read_only_fields = ('legal_name', 'managers', 'owners')
