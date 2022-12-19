from django.db import models

from .utils import upload_directory_path


class Sensor(models.Model):
    # id = pk
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    description = models.CharField(max_length=200, null=True, verbose_name='Описание')
    # measurements

    class Meta:
        verbose_name = 'Датчик'
        verbose_name_plural = 'Датчики'
        ordering = ['name']

    def __str__(self):
        return f'Датчик {self.pk}: {self.name}'


class Measurement(models.Model):
    # id = pk
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='measurements', verbose_name='Датчик')
    measurement = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Измерение')
    measurement_time = models.DateTimeField(auto_now=True, verbose_name='Время измерения')
    snapshot = models.ImageField(upload_to=upload_directory_path, null=True, blank=True, verbose_name='Снимок')

    class Meta:
        verbose_name = 'Измерение'
        verbose_name_plural = 'Измерения'
        ordering = ['-measurement_time']

    def __str__(self):
        return f'Измерение {self.pk} |  Датчик {self.sensor.pk}: {self.sensor.name} | {self.measurement}'
