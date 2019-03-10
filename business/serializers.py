from rest_framework import serializers


class PublicBusinessSerializer(serializers.ModelSerializer):
    from location.serializers import StateSerializer

    state = StateSerializer(many=False)

    class Meta:
        from .models import Business

        model = Business
        fields = ('id', 'name', 'gst', 'pan', 'state', 'fssai', 'legal_name')


class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import Business

        model = Business
        fields = ('id', 'name', 'business_type', 'gst', 'pan', 'state',
                  'fssai', 'is_active', 'legal_name')
        read_only_fields = ('legal_name',)
