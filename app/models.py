from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=256)
    author = models.ForeignKey('Author', max_length=256, on_delete=models.PROTECT)
    date_written = models.DateField(null=True, blank=True)
    genre = models.ForeignKey('Genre', related_name='books')


class Author(models.Model):
    name = models.CharField(max_length=256)
    surname = models.CharField(max_length=256)
    birth_date = models.DateField()
    death_date = models.DateField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)


class Genre(models.Model):
    name = models.CharField(max_length=256)


class BookInstance(models.Model):
    book = models.ForeignKey('Book', on_delete=models.PROTECT)
    user = models.ForeignKey(User,on_delete=models.PROTECT)

    STATUS_CHOICES = (
        ('m', 'Maintenance'),
        ('a', 'Avaible'),
        ('t', 'Taken'),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='m')

    due_date = models.DateField()