from django.shortcuts import render

from articles.models import Article


def articles_list(request):
    template = 'articles/news.html'
    # ordering = '-published_at'  # Сортировка по умолчанию прописана в Meta классе модели

    article_list = Article.objects.all()
    context = {'object_list': article_list}

    return render(request, template, context)
