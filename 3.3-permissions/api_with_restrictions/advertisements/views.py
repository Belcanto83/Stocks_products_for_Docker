from django.shortcuts import redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement
from advertisements.pagination import AdvertisementPagination
from advertisements.permissions import IsOwnerOrReadOnly
from advertisements.serializers import AdvertisementSerializer


def index(request):
    return redirect('admin/')


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    # настраиваем ViewSet, указываем атрибуты для кверисета, сериализаторов, фильтров и паджинатора
    queryset = Advertisement.objects.order_by('-updated_at')
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter
    pagination_class = AdvertisementPagination

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return []
