import json

import django
from django.db import models
from django.core.management.base import BaseCommand
from school.models import Teacher, Student


class Command(BaseCommand):
    help = 'Загрузить данные в базу из файла(ов). Названия файлов указываются через пробел'
    models_map = {
        'school.teacher': Teacher,
        'school.student': Student,
    }

    def add_arguments(self, parser):
        parser.add_argument('path', nargs='+', type=str)

    def handle(self, *args, **options):
        """
        Заполняет базу данных содержимым из .json файла(ов).
        """

        def get_model_foreign_keys():
            foreign_keys = []
            for field in Model._meta.fields:
                if isinstance(field, models.ForeignKey):
                    foreign_keys.append(field.name)
            if not foreign_keys:
                return None
            return foreign_keys

        for file in options['path']:
            try:
                with open(file, 'r', encoding='UTF-8') as f:
                    data = json.load(f)
                for item in data:
                    Model = self.models_map.get(item['model'])
                    try:
                        f_keys = get_model_foreign_keys()
                        if f_keys is None:
                            Model.objects.create(id=item['pk'], **item['fields'])
                        else:
                            f_keys_dict = {}
                            for f_key in f_keys:
                                RelModel = Model._meta.get_field(f_key).related_model
                                RelObj = RelModel.objects.get(id=item['fields'][f_key])
                                f_keys_dict[f_key] = RelObj
                            not_f_keys_dict = {}
                            for key in item['fields']:
                                if key not in f_keys_dict:
                                    not_f_keys_dict[key] = item['fields'][key]
                            Model.objects.create(id=item['pk'], **f_keys_dict, **not_f_keys_dict)
                    except django.db.utils.IntegrityError:
                        print(f'Данные (model={item["model"]}, id={item["pk"]}) уже есть в базе данных!')
                print(f'Новые данные из файла {file} были успешно добавлены в базу!')
            except FileNotFoundError as err:
                print(err)
            except django.db.utils.OperationalError:
                print('Ошибка подключения к базе данных.. :(')
