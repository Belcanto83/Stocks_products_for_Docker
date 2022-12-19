from rest_framework import serializers

from .models import Measurement, Sensor


class MeasurementSerializer(serializers.ModelSerializer):
    temperature = serializers.DecimalField(source='measurement', max_digits=5, decimal_places=2)
    created_at = serializers.DateTimeField(source='measurement_time', read_only=True)

    class Meta:
        model = Measurement
        fields = ['id', 'temperature', 'created_at', 'sensor', 'snapshot']


class MeasurementMinDetailSerializer(serializers.ModelSerializer):
    temperature = serializers.DecimalField(source='measurement', max_digits=5, decimal_places=2)
    created_at = serializers.DateTimeField(source='measurement_time', read_only=True)

    class Meta:
        model = Measurement
        fields = ['temperature', 'created_at', 'snapshot']


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description']


class SensorDetailSerializer(serializers.ModelSerializer):
    measurements = MeasurementMinDetailSerializer(read_only=True, many=True, required=False)

    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description', 'measurements']
