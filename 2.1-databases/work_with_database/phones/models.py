from django.db import models


class Phone(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True, editable=True)
    name = models.CharField(max_length=50)
    image = models.URLField(max_length=200)
    price = models.PositiveIntegerField()
    release_date = models.DateField()
    lte_exists = models.BooleanField()
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name
