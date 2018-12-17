from rest_framework import serializers


class PublicBusinessSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import Business

        model = Business
        fields = ('id', 'name', 'gst', 'pan', 'state__name', 'fssai')
