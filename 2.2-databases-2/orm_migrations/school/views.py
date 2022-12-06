from django.views.generic import ListView
from django.shortcuts import render, HttpResponse
from django.db.utils import OperationalError

from .models import Student


def students_list(request):
    template = 'school/students_list.html'
    try:
        ordering = 'group'
        students = Student.objects.order_by(ordering).prefetch_related('teachers')
        context = {'students': students}
        return render(request, template, context)
    except OperationalError:
        return HttpResponse('Ошибка подключения к базе данных..')
