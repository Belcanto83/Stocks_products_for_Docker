
def upload_directory_path(instance, filename):
    return f'{instance.measurement_time.year}/{instance.measurement_time.month}/{instance.measurement_time.day}/' \
           f'{instance.sensor_id}/{filename}'
