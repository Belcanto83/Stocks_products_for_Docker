from django.urls import path

from .views import SensorListCreateAPIView, SensorDetailAPIView, MeasurementListCreateAPIView

urlpatterns = [
    # TODO: зарегистрируйте необходимые маршруты
    path('sensors/', SensorListCreateAPIView.as_view(), name='sensors'),
    path('sensors/<int:pk>/', SensorDetailAPIView.as_view(), name='sensor_detail'),
    path('measurements/', MeasurementListCreateAPIView.as_view(), name='measurements'),
]
