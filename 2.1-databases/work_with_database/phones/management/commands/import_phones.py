import csv
import re

import django
from django.core.management.base import BaseCommand
from phones.models import Phone


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        """
        Заполняет базу данных содержимым из .csv файла.
        В данный момент создается и заполняется данными только 1 таблица..
        """
        def _create_slug_field(name):
            slug_str = re.sub(r'[^\w\d]+', '-', name.strip())
            return slug_str.lower()

        with open('phones.csv', 'r') as file:
            phones = list(csv.DictReader(file, delimiter=';'))

        try:
            for phone in phones:
                Phone.objects.create(**phone, slug=_create_slug_field(phone.get('name')))
            print('Данные были успешно добавлены в базу данных!')
        except django.db.utils.IntegrityError:
            print('Эти данные уже есть в базе данных!')
