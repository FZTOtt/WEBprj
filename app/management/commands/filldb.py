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
        self.create_like(200 * ratio)

    def create_users(self, ratio):
        for i in range(ratio):
            User.objects.create_user(username=get_random_string(10), password='123')
        print("User_Okey")

    def create_tags(self, ratio):
        tags = (Tag(title=get_random_string(12)
                    ) for i in range(ratio))
        while True:
            new = list(islice(tags, 60))

            if not new:
                break
            Tag.objects.bulk_create(new, 60)
        print("Tags_Okey")

    def create_questions(self, ratio):

        authors = list(User.objects.values_list('id', flat=True))
        questions = (Question(author=User.objects.all().get(id=random.choice(authors)),
                              title=f().sentence()[:40],
                              body='. '.join(f().sentences(f().random_int(min=1, max=3))),
                              rating=f().random_int(min=0, max=10)
                              ) for i in range(ratio))
        while True:
            new = list(islice(questions, 60))
            if not new:
                break
            Question.objects.bulk_create(new, 60)

        tags = list(Tag.objects.values_list('id', flat=True))
        questions = Question.objects.all()
        for question in questions:
            for i in range(f().random_int(min=0, max=4)):
                question.tags.add(random.choice(tags))
        print("Question_Okey")

    def create_answers(self, ratio):
        # new_ratio = 45000
        authors = list(User.objects.values_list('id', flat=True))
        questions = list(Question.objects.values_list('id', flat=True))
        answers = (Answer(author=User.objects.all().get(id=random.choice(authors)),
                          question=Question.objects.all().get(id=random.choice(questions)),
                          text='. '.join(f().sentences(f().random_int(min=1, max=3))),
                          rating=f().random_int(min=0, max=10)
                          ) for i in range(ratio))
        # print()
        print("Start answer")
        while True:
            new = list(islice(answers, 100))
            if not new:
                break
            Answer.objects.bulk_create(new, 100)
        print("Answer_Okey")

    def create_like(self, ratio):
        user = User.objects.all()
        print('Users selected')
        count = 0
        for question in Question.objects.all():
            for i in range(f().random_int(min=0, max=4)):
                # if count > ratio / 2:
                #     continue
                # else:
                    like = Like()
                    like.user = random.choice(user)
                    like.vote = 1
                    like.content_object = question
                    if Like.objects.filter(user_id=like.user.pk, content_type_id=8, object_id=question.pk).exists():
                        print('like is exist')
                        continue
                    else:
                        like.save()
                    count += count
            print(f'save question{question.title}')
            question.save()

        count = 0
        for answer in Answer.objects.all():
            for i in range(f().random_int(min=0, max=4)):
                # if count > ratio / 2:
                #     continue
                # else:
                like = Like()
                like.user = random.choice(user)
                like.vote = 1
                like.content_object = answer
                if Like.objects.filter(user_id=like.user.pk, content_type_id=9, object_id=answer.pk).exists():
                    print('like is exist')
                    continue
                else:
                    like.save()
                count += 1
            print(f'{count}')

            answer.save()

        print("Likes_Okey")
