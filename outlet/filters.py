from drfaddons.filters import IsOwnerFilterBackend


class IsOwnerOrManagerFilterBackend(IsOwnerFilterBackend):

    def filter_queryset(self, request, queryset, view):
        from django.db.models import Q

        return queryset.filter(Q(outlet__manager=request.user) | Q(created_by=request.user)).distinct()
