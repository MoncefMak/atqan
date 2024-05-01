from rest_framework import permissions


class CreateProductPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.has_perm('product.add_product')
