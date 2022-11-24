from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse

import csv


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице

    page_number = request.GET.get('page', 1)

    # Получаем данные из "csv" файла
    with open('data-398-2018-08-30.csv', encoding='utf-8') as f:
        rows_iterator = csv.DictReader(f, delimiter=',')
        rows = list(rows_iterator)

    chunk_size = 10
    paginator = Paginator(rows, chunk_size)
    page = paginator.get_page(page_number)

    bus_stations = [{'Name': itm.get('Name'), 'Street': itm.get('Street'), 'District': itm.get('District')}
                    for itm in page]

    context = {
        'bus_stations': bus_stations,
        'page': page,
    }
    return render(request, 'stations/index.html', context)
