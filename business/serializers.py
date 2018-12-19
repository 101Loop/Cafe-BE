from rest_framework import serializers


class PublicBusinessSerializer(serializers.ModelSerializer):
    state = serializers.CharField(source='state.name', read_only=True)

    class Meta:
        from .models import Business

        model = Business
        fields = ('id', 'name', 'gst', 'pan', 'state', 'fssai')
