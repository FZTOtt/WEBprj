from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models import Sum
from django.contrib.contenttypes.fields import GenericRelation

# Create your models here.
# class Profile(models.Model):
#     User_id = models.ForeignKey('User', related_name='id')
#     Name = models.CharField(max_length=256)
#     Profile_photo = models.ImageField()
#     About = models.CharField(max_length=2000)


# class customUser(AbstractUser):
#     #avatar = models.ImageField(default=None, upload_to='static/main/upload/')
#     rating = models.IntegerField(default=0, verbose_name='User rating')

class QuestionManager(models.Manager):
    # def hottest(self):
    #     return self.order_by()

    def id(self, search_id):
        return self.all().filter(id=search_id)
    def newest(self):
        return self.all().order_by('date').reverse()


class LikeManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        return self.get_queryset().filter(vote__lt=0)

    def sum_rating(self):
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0


class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    body = models.TextField()
    tags = models.ManyToManyField('Tag', related_name='questions', verbose_name='Tags')
    date = models.DateTimeField(default=timezone.now)
    votes = GenericRelation('Like', related_query_name='questions')
    solved = models.BooleanField(default=False)
    objects = QuestionManager()

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self):
        return self.title


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    status = models.BooleanField(default=False) #sidkier or not


class Tag(models.Model):
    title = models.CharField(max_length=40, unique=True)
    #rating = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Like(models.Model):
    LIKE = 1
    DISLIKE = -1
    TYPES = ((LIKE, 1), (DISLIKE, -1))

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote = models.SmallIntegerField(choices=TYPES, verbose_name='like')
    content_type = models.ForeignKey(ContentType, default=None, on_delete=models.CASCADE)
    content_object = GenericForeignKey()
    objects = LikeManager()
    object_id = models.PositiveIntegerField(default=-1)


    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'

    # def __str__(self):
    #     return self.user.username

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