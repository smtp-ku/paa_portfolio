from rest_framework import permissions


class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_superuser:
            return True
        else:
            return False

        # if view.action == 'list':
        #     return request.user.is_authenticated and request.user.is_superuser
        # elif view.action == 'create':
        #     return True
        # elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
        #     return True
        # else:
        #     print('aaa'+str(view.action))
        #     return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user.is_superuser:
            return True
        else:
            return False
