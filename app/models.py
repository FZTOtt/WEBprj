from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# Create your models here.
# class Profile(models.Model):
#     User_id = models.ForeignKey('User', related_name='id')
#     Name = models.CharField(max_length=256)
#     Profile_photo = models.ImageField()
#     About = models.CharField(max_length=2000)


class User(AbstractUser):
    #avatar = models.ImageField(default=None, upload_to='static/main/upload/')
    rating = models.IntegerField(default=0, verbose_name='User rating')

    # class Meta:
    #     verbose_name = 'User'
    #     verbose_name_plural = 'Users'
    #
    # def __str__(self):
    #     return self.username

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    body = models.TextField()
    tags = models.ManyToManyField('Tag', related_name='questions')
    date = models.DateTimeField(default=timezone.now)
    solved = models.BooleanField(default=False)


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    status = models.BooleanField(default=False) #sidkier or not


class Tag(models.Model):
    title = models.CharField(max_length=40, unique=True)


#class Like(models.Model):
#    user = models.ForeignKey(User, on_delete=models.CASCADE)

# class Book(models.Model):
#     title = models.CharField(max_length=256)
#     author = models.ForeignKey('Author', max_length=256, on_delete=models.PROTECT)
#     date_written = models.DateField(null=True, blank=True)
#     genre = models.ManyToManyField('Genre', related_name='books')
#
#
# class Author(models.Model):
#     name = models.CharField(max_length=256)
#     surname = models.CharField(max_length=256)
#     birth_date = models.DateField()
#     death_date = models.DateField(null=True, blank=True)
#     is_deleted = models.BooleanField(default=False)
#
#
# class Genre(models.Model):
#     name = models.CharField(max_length=256)
#
#
# class BookInstance(models.Model):
#     book = models.ForeignKey('Book', on_delete=models.PROTECT)
#     user = models.ForeignKey(User,on_delete=models.PROTECT)
#
#     STATUS_CHOICES = (
#         ('m', 'Maintenance'),
#         ('a', 'Avaible'),
#         ('t', 'Taken'),
#     )
#     status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='m')
#
#     due_date = models.DateField()