import psycopg2
from psycopg2 import sql

from django.conf import settings

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        """
        Команда создает новую базу данных PostgreSQL.
        Имя новой базы данных задается в файле конфигурации проекта 'settings.py' в разделе 'DATABASES'.
        """

        data_base = settings.DATABASES
        try:
            con = psycopg2.connect(
                database='postgres',
                user=data_base['default'].get('USER'),
                password=data_base['default'].get('PASSWORD')
            )
            con.autocommit = True

            new_db_name = data_base['default'].get('NAME')
            cur = con.cursor()
            try:
                cur.execute(
                    sql.SQL("CREATE DATABASE {}").format(sql.Identifier(new_db_name))
                )
            except psycopg2.errors.DuplicateDatabase:
                print(f'База данных с именем "{new_db_name}" уже существует!')
            con.close()
            print('Успех!')
        except psycopg2.OperationalError:
            print('Ошибка подключения к базе данных!')