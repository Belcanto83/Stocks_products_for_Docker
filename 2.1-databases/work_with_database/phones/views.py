from django.shortcuts import render, redirect

from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request, sort='name'):
    template = 'catalog.html'

    phones = Phone.objects.all()

    reverse = False
    sort_param = request.GET.get('sort', sort)
    if sort_param == 'min_price':
        sort_field = 'price'
    elif sort_param == 'max_price':
        sort_field = 'price'
        reverse = True
    else:
        sort_field = sort_param

    sorted_phones = sorted(phones, key=lambda itm: itm.__getattribute__(sort_field), reverse=reverse)

    context = {'phones': sorted_phones}
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phone = Phone.objects.get(slug=slug)
    context = {'phone': phone}
    return render(request, template, context)
