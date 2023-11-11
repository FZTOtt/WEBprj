import random
from itertools import islice
from faker import Faker as f
from django.core.management.base import BaseCommand
from app.models import Question, Answer, Tag, Like, User
from django.utils.crypto import get_random_string


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']
        self.create_users(ratio)
        self.create_tags(ratio)
        self.create_questions(10 * ratio)
        self.create_answers(100 * ratio)
        self.create_likes(200 * ratio)

    def create_users(self, ratio):
        ratio = 7050
        for i in range(ratio):
            User.objects.create_user(username=get_random_string(10), password='123')
        print("User_Okey")

    def create_tags(self, ratio):
        tags = (Tag(title=get_random_string(10)
                    ) for i in range(ratio))
        while True:
            new = list(islice(tags, ratio))

            if not new:
                break
            Tag.objects.bulk_create(new, ratio)
        print("Tags_Okey")

    def create_questions(self, ratio):
        authors = list(User.objects.values_list('id', flat=True))
        questions = (Question(author=User.objects.all().get(id=random.choice(authors)),
                              title=get_random_string(20),
                              body=get_random_string(120),
                              rating=f().random_int(min=0, max=50)
                              ) for i in range(ratio))
        while True:
            new = list(islice(questions, ratio))
            if not new:
                break
            Question.objects.bulk_create(new, ratio)

        tags = list(Tag.objects.values_list('id', flat=True))
        questions = Question.objects.all()
        for question in questions:
            for i in range(f().random_int(min=0, max=4)):
                question.tags.add(random.choice(tags))
        print("Question_Okey")

    def create_answers(self, ratio):
        authors = list(User.objects.values_list('id', flat=True))
        questions = list(Question.objects.values_list('id', flat=True))
        answers = (Answer(author=User.objects.all().get(id=random.choice(authors)),
                          question=Question.objects.all().get(id=random.choice(questions)),
                          text=get_random_string(120),
                          rating=f().random_int(min=0, max=50)
                          ) for i in range(ratio))
        while True:
            new = list(islice(answers, ratio))
            if not new:
                break
            Answer.objects.bulk_create(new, ratio)
        print("Answer_Okey")

    def create_likes(self, ratio):
        user = User.objects.all()
        count = 0
        for question in Question.objects.all():
            for i in range(f().random_int(min=0, max=4)):
                if count > ratio / 2:
                    continue
                else:
                    like = Like()
                    like.user = random.choice(user)
                    like.vote = 1
                    like.content_object = question
                    like.save()
                    count += count
            question.save()
        count = 0
        for answer in Answer.objects.all():
            for i in range(f().random_int(min=0, max=4)):
                if count > ratio / 2:
                    continue
                else:
                    like = Like()
                    like.user = random.choice(user)
                    like.vote = 1
                    like.content_object = answer
                    like.save()
                    count += count
            answer.save()
        print("Likes_Okey")
