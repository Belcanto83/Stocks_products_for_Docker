from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Разрешаем все действия для админов (user.is_staff==True)
        if request.user.is_staff:
            return True
        return request.user == obj.creator


# class CanReadDrafts(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         # Разрешаем все действия для админов (user.is_staff==True)
#         if request.user.is_staff:
#             return True
#         return obj.status != AdvertisementStatusChoices.DRAFT or request.user == obj.creator
