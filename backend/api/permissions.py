from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Разрешает только безопасные методы.
    Позволяет всем пользователям читать данные.
    Разрешает создавать, изменять и удалять данные только их автору.
    """

    def has_permission(
            self,
            request,
            view
    ):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(
            self,
            request,
            view,
            obj
    ):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
