from rest_framework import serializers


class PublicBusinessSerializer(serializers.ModelSerializer):
    from location.serializers import StateSerializer

    state = StateSerializer(many=False)

    class Meta:
        from .models import Business

        model = Business
        fields = ('id', 'name', 'gst', 'pan', 'state', 'fssai', 'legal_name')
