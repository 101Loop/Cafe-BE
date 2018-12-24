from rest_framework.permissions import BasePermission

from drf_user.models import User


def is_manager(user: User)->bool:
    from .models import OutletManager

    return OutletManager.objects.filter(manager=user).count() > 0


def is_owner(user: User)->bool:
    from .models import Outlet

    return Outlet.objects.filter(created_by=user).count() > 0


class IsOwner(BasePermission):

    def has_permission(self, request, view)->bool:
        return super(IsOwner, self).has_permission(request, view) and is_owner(request.user)


class OwnerOrManager(IsOwner):

    def has_permission(self, request, view):
        return is_manager(request.user)

    def has_object_permission(self, request, view, obj):
        from .models import OutletManager

        if isinstance(obj, OutletManager):
            if is_manager(request.user):
                return request.user in obj.outlet.outletmanager_set.all()
            if is_manager(request.user):
                return request.user.id is obj.outlet.created_by_id
