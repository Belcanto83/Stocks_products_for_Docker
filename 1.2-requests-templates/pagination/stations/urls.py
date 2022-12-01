from django.urls import path

from .views import index, show_bus_stations

urlpatterns = [
    path('', index, name='index'),
    path('bus_stations/', show_bus_stations, name='bus_stations'),
]
