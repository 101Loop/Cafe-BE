from drfaddons.generics import RetrieveUpdateByUserAPIView

from rest_framework.generics import ListAPIView


class ListCategoryView(ListAPIView):
    from rest_framework.permissions import AllowAny

    from .models import CategoryMaster
    from .serializers import CategoryMasterSerializer

    queryset = CategoryMaster.objects.all()
    serializer_class = CategoryMasterSerializer

    permission_classes = (AllowAny, )
    filter_backends = ()


class UserProfileView(RetrieveUpdateByUserAPIView):
    """
    User Profile

    Provides necessary info about user
    """
    from .models import UserProfile
    from .serializers import UserProfileSerializer

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
