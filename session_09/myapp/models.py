from django.db import models
from django.utils import timezone


class Item(models.Model):
    name = models.CharField(max_length=100)
    value = models.IntegerField()

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateField()

    def summary(self) -> str:
        return self.content[:100]

    def is_published(self) -> bool:
        return self.published_date <= timezone.now().date()

    def __str__(self):
        return self.title
