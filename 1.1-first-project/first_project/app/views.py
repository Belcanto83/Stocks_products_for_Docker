from django.http import HttpResponse
from django.shortcuts import render, reverse

from datetime import datetime
import os


def home_view(request):
    template_name = 'app/home.html'
    pages = {
        'Главная страница': reverse('home'),
        'Показать текущее время': reverse('time'),
        'Показать содержимое рабочей директории': reverse('workdir')
    }
    context = {
        'pages': pages
    }
    return render(request, template_name, context)


def time_view(request):
    msg = '<a href="/">На главную</a><br>'
    current_time = datetime.now().time().strftime("%H:%M:%S")
    msg += f'Текущее время: {current_time}'
    return HttpResponse(msg)


def workdir_view(request):
    # dir_list = os.listdir('.')

    # вывести список всех файлов и каталогов РЕКУРСИВНО
    # def _recursive_generator(path):
    #     entries = os.listdir(path)
    #     for entry in entries:
    #         entry_with_path = os.path.join(path, entry)
    #         if not os.path.isdir(entry_with_path):
    #             yield entry_with_path
    #         else:
    #             # yield entry_with_path  # вывод имен каталогов (если нужно) в том числе, а не только имен файлов
    #             yield from _recursive_generator(entry_with_path)

    # вывести список всех файлов и каталогов РЕКУРСИВНО (можно задать список игнорируемых каталогов)
    def _recursive_generator_2(path, ignore_list=None):
        entries = os.listdir(path)
        for entry in entries:
            if ignore_list and entry not in ignore_list:
                entry_with_path = os.path.join(path, entry)
                if not os.path.isdir(entry_with_path):
                    yield entry_with_path
                else:
                    # yield entry_with_path  # вывод имен каталогов (если нужно) в том числе, а не только имен файлов
                    yield from _recursive_generator_2(entry_with_path, ignore_list)
            else:
                continue

    def generate_response(path):
        result_str = '<a href="/">На главную</a><br>'
        for itm in _recursive_generator_2(path, ignore_list=['venv', 'app']):
            result_str += itm + '<br>'
        return result_str

    root_path = '.'
    response_str = generate_response(root_path)

    return HttpResponse(response_str)
