from rest_framework import serializers


class ShowMenuSerializer(serializers.Serializer):

    class Meta:
        from .models import Menu
        model = Menu
        fields = '__all__'
