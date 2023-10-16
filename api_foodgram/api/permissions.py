from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrReadOnly(BasePermission):
    """Разрешение только для автора или только на чтение."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user


class IsAuthorizedAndAuthor(BasePermission):
    """Доступ только для авторизированного автора."""

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.author == request.user
