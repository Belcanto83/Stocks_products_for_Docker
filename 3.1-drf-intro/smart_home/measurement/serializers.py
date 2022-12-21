import io

from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

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


############################################################################################################
# Вспомогательная информация (данный код не используется в этом проекте)
# Понимание принципа сериализации и десериализации объектов в DRF

def encode():
    # Создаем объект модели Sensor
    sensor_obj = Sensor(name='Test sensor', description='We are just testing encode function')
    # Создаем из модели объект сериализатора
    model_serializer = SensorSerializer(sensor_obj)
    print('model_serializer:', model_serializer)
    print('type(model_serializer):', type(model_serializer))
    # Получаем сериализованные (обработанные) данные: спец. словарь
    data = model_serializer.data
    print('Сериализованные данные:', data)
    print('Тип сериализованных данных:', type(data))
    # Превращаем сериализованные (обработанные сериализатором) данные (спец. словарь) в байтовую строку
    # Наконец, данные в байтах передаются клиенту в сеть (например, в http-ответе)
    json_str = JSONRenderer().render(data)
    print('Строка байт:', json_str)
    print('Тип байтовой строки:', type(json_str))


def decode():
    # Получаем "сырые" данные в байтах (например, из http-запроса от клиента)
    raw_bytes = b'{"name":"Test sensor","description":"We are just testing encode function"}'
    # "Обернем" байтовую строку в объект BytesIO
    stream = io.BytesIO(raw_bytes)
    # Преобразуем "сырые" байтовые данные в обычный словарь языка "Пайтон"
    dict_data = JSONParser().parse(stream)
    print('Распарсенные данные:', dict_data)
    print('Тип распарсенных данных:', type(dict_data))
    # Создаем объект сериализатора и передаем в него наш словарь
    model_serializer = SensorSerializer(data=dict_data)
    # Проверяем распарсенные данные на соответствие ограничениям модели
    model_serializer.is_valid(raise_exception=True)
    # Получаем проверенные сериализатором данные
    validated_data = model_serializer.validated_data
    print('Десериализованные данные:', validated_data)
    print('Тип десериализованных данных:', type(validated_data))
    # Можем создать модель Sensor, используя полученные десериализованные данные
    sensor_obj = Sensor(**validated_data)
    print('Модель Sensor:', sensor_obj)
    print('Тип модели Sensor:', type(sensor_obj))
