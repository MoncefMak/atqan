from rest_framework import permissions


class CreateUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST' and not request.user.is_authenticated:
            return True
        if request.user.is_authenticated and request.method == 'POST' and request.user.has_perm('accounts.add_user'):
            return True
        return False


class UpdateUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.method in ['PUT', 'PATCH'] and request.user.has_perm('accounts.change_user'):
            obj = view.get_object()
            if obj and obj.groups.filter(name='Client').exists():
                return True
        return False


class DeleteUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.method == 'DELETE' and request.user.has_perm('accounts.delete_user'):
            obj = view.get_object()
            if obj and obj.groups.filter(name='Client').exists():
                return True
        return False


class GetUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.method == 'GET' and request.user.has_perm('accounts.view_user'):
            return True
        return False
