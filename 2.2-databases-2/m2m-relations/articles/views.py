from django.shortcuts import render

from articles.models import Article


def articles_list(request):
    template = 'articles/news.html'
    # ordering = ['-published_at', 'title']  # Сортировка по умолчанию прописана в Meta классе модели "Article"

    article_list = Article.objects.all().prefetch_related('scopes__tag')
    context = {'object_list': article_list}

    return render(request, template, context)
