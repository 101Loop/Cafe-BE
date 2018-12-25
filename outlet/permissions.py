from rest_framework.permissions import IsAuthenticated

from drf_user.models import User


def is_manager(user: User)->bool:
    from .models import OutletManager

    return OutletManager.objects.filter(manager=user, is_active=True).count() > 0


def is_owner(user: User)->bool:
    from .models import Outlet

    return Outlet.objects.filter(created_by=user).count() > 0


class IsOutletOwner(IsAuthenticated):

    def has_permission(self, request, view)->bool:
        return super(IsOutletOwner, self).has_permission(request, view) and is_owner(request.user)

    def has_object_permission(self, request, view, obj):
        from .models import Outlet

        from order.models import Order

        if isinstance(obj, Order):
            obj = obj.outlet

        if isinstance(obj, Outlet):
            return obj.created_by == request.user


class IsManager(IsAuthenticated):

    def has_permission(self, request, view):
        return (super(IsManager, self).has_permission(request=request,
                                                      view=view)
                and is_manager(request.user))

    def has_object_permission(self, request, view, obj):
        from .models import Outlet

        from order.models import Order

        if isinstance(obj, Order):
            obj = obj.outlet

        if isinstance(obj, Outlet):
            return (request.user.id in obj.outletmanager_set
                    .filter(is_active=True)
                    .values_list('manager', flat=True))


class OwnerOrManager(IsAuthenticated):

    def has_permission(self, request, view):
        return (IsOutletOwner().has_permission(request=request, view=view)
                or IsManager().has_permission(request=request, view=view))

    def has_object_permission(self, request, view, obj):
        return (IsOutletOwner().has_object_permission(request=request,
                                                      view=view, obj=obj)
                or IsOutletOwner().has_object_permission(request=request,
                                                         view=view, obj=obj))
