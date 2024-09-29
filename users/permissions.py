from rest_framework import permissions


class IsUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        """Проверка, авторизации пользователя"""
        if obj.email == request.user.email:
            return True
        return False
