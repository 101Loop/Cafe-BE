from rest_framework import serializers


class OCPointWalletSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import OCPointWallet

        model = OCPointWallet
        fields = ('id', 'points')
        read_only_fields = fields


class OCPointWalletTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import OCPointTransaction

        model = OCPointTransaction
        fields = ('id', 'payment', 'value', 'is_credit')
        read_only_fields = fields
