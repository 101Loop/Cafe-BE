from rest_framework import serializers
from .models import User


class UserShowSerializer(serializers.ModelSerializer):
    """
    UserShowSerializer is a model serializer which shows the attributes of a user.

    Returns
    -------
     tuple
        Returns a tuple containing::
                data = dict
                    This is a dictionary containing::
                        'username' : str
                        'name' : str
    Examples
    --------
    >>> print(UserShowSerializer(data = {'username':'test@testing.com', 'name':'test'}))
    UserShowSerializer(data={'username': 'test@testing.com', 'name': 'test'}):
    username = CharField(label='Unique UserName', read_only=True)
    name = CharField(label='Full Name', read_only=True)
    """

    class Meta:
        model = User
        fields = ('username', 'name')
        read_only_fields = ('username', 'name')


class LoginOTPSerializer(serializers.Serializer):
    mobile = serializers.CharField(min_length=10, max_length=13)
    otp = serializers.CharField(min_length=4, max_length=4, default=None)
    email = serializers.EmailField(min_length=6, default=None)


class UpdateProfileSerializer(serializers.ModelSerializer):
    """
    This model serializer is to update the profile of a user.
    """

    email = serializers.EmailField(required=False)
    mobile = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    organization = serializers.CharField(required=False)

    class Meta:

        from .models import User

        model = User
        fields = ('name', 'email', 'mobile', 'organization')
