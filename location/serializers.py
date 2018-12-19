from rest_framework import serializers


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        from .models import Country

        model = Country
        fields = ('id', 'name')


class StateSerializer(serializers.ModelSerializer):
    country = CountrySerializer(many=False, read_only=True)

    class Meta:
        from .models import State

        model = State
        fields = ('id', 'name', 'country')


class CitySerializer(serializers.ModelSerializer):
    state = StateSerializer(many=True, read_only=True)

    class Meta:
        from .models import City

        model = City
        fields = ('id', 'name', 'state')
