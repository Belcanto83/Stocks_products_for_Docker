import django
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Book

from datetime import datetime


def index(request):
    return redirect('books')


def books_view(request):
    template = 'books/books_list.html'
    try:
        books = Book.objects.all().order_by('name')
        context = {'books': books}
        return render(request, template, context)
    except django.db.utils.OperationalError:
        return HttpResponse('Ошибка подключения к базе данных.. :(')


def pub_date_view(request, date):
    template = 'books/books_by_pub_date.html'
    date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    try:
        books = Book.objects.filter(pub_date=date_obj)

        pub_dates_dict_list = list(Book.objects.order_by('pub_date').distinct('pub_date').values('pub_date'))
        pub_dates = [list(d.values())[0] for d in pub_dates_dict_list]
        ind = pub_dates.index(date_obj)

        context = {
            'date': date,
            'previous_page': pub_dates[ind-1].strftime('%Y-%m-%d') if ind > 0 else None,
            'next_page': pub_dates[ind+1].strftime('%Y-%m-%d') if ind < len(pub_dates) - 1 else None,
            'books': books
        }
        return render(request, template, context)
    except django.db.utils.OperationalError:
        return HttpResponse('Ошибка подключения к базе данных.. :(')
