from django.db import models


class Article(models.Model):
    # id
    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации', auto_now_add=True)
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение')
    # tags
    # scopes

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-published_at', 'title']

    def __str__(self):
        return self.title


class Tag(models.Model):
    # id
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_created=True)
    articles = models.ManyToManyField(Article, related_name='tags', through='Scope', verbose_name='Статьи')
    # scopes

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['name']

    def __str__(self):
        return self.name


class Scope(models.Model):
    # id
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='scopes', verbose_name='Статья')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='scopes', verbose_name='Тег')
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    is_main = models.BooleanField(verbose_name='Основной')

    class Meta:
        verbose_name = 'Связанный объект'
        verbose_name_plural = 'Связанные объекты'
        ordering = ['-is_main', 'tag']
        constraints = [
            models.UniqueConstraint(fields=['article', 'tag'], name='article_tags')
        ]
        # unique_together = ('article', 'tag')  # deprecated

    def __str__(self):
        return f'<Связанный объект>:  "Статья: {self.article}" <---> "Тег: {self.tag}"'
