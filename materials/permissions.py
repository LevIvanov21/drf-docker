from rest_framework import permissions


class IsModerator(permissions.BasePermission):

    def has_permission(self, request, view):
        """Проверяет, что пользователь в группе 'модератор'"""
        return request.user.groups.filter(name='модератор').exists()


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        """Проверяет, что пользователь является владельцем"""
        if obj.owner == request.user:
            return True
        return False
