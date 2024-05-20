from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=50, unique=True)

class Book(models.Model):
    title = models.CharField(max_length=50, unique=True)
    quantity = models.IntegerField(default=1)
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING)