import json

import django
from django.core.management.base import BaseCommand
from books.models import Book


class Command(BaseCommand):
    help = 'Загрузить данные в базу из файла(ов). Названия файлов указываются через пробел'
    models_map = {'books.book': Book}

    def add_arguments(self, parser):
        parser.add_argument('path', nargs='+', type=str)

    def handle(self, *args, **options):
        """
        Заполняет базу данных содержимым из .json файла.
        В данный момент создается и заполняется данными только 1 таблица..
        """

        for file in options['path']:
            try:
                with open(file, 'r', encoding='UTF-8') as f:
                    books = json.load(f)
                for book in books:
                    Model = self.models_map.get(book['model'])
                    try:
                        Model.objects.create(id=book['pk'], **book['fields'])
                    except django.db.utils.IntegrityError:
                        print(f'Данные (model={book["model"]}, id={book["pk"]}) уже есть в базе данных!')
                print(f'Новые данные из файла {file} были успешно добавлены в базу!')
            except FileNotFoundError as err:
                print(err)
            except django.db.utils.OperationalError:
                print('Ошибка подключения к базе данных.. :(')
