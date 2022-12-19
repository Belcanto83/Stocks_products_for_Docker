from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import SensorListCreateAPIView, SensorDetailAPIView, MeasurementListCreateAPIView

urlpatterns = [
    path('sensors/', SensorListCreateAPIView.as_view(), name='sensors'),
    path('sensors/<int:pk>/', SensorDetailAPIView.as_view(), name='sensor_detail'),
    path('measurements/', MeasurementListCreateAPIView.as_view(), name='measurements'),
]
