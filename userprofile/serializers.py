from rest_framework import serializers


class CategoryMasterSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import CategoryMaster

        model = CategoryMaster
        fields = ('id', 'name', 'point', 'is_percentage')
        read_only_fields = fields


class UserProfileSerializer(serializers.ModelSerializer):
    from currency.serializers import OCPointWalletSerializer

    category = CategoryMasterSerializer(many=False, read_only=True)
    wallet = OCPointWalletSerializer(source='get_wallet_info', many=False,
                                     read_only=True)

    def get_wallet_info(self, obj):
        from currency.models import OCPointWallet

        return OCPointWallet.objects.get(created_by_id=obj.created_by.id)

    class Meta:
        from .models import UserProfile

        model = UserProfile
        fields = ('id', 'category', 'company', 'designation', 'wallet')
        read_only_fields = ('id', 'category', )
