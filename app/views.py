from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponseBadRequest, HttpResponse
from django.views import View
import json
from .models import *
from django.http import Http404

# Create your views here.
# QUESTIONS = [
#         {
#         'id': i,
#         'title': f'Question {i}',
#         'content': f'Please, help me {i}'
#     } for i in range (20)
#     ]
#
#
# ANSWERS = [
#         {
#         'id': i,
#         'title': f'Answer {i}',
#         'content': f'Let me help you {i}'
#     } for i in range (20)
#     ]


def tag(request, tag_name):
    tag_questions = []
    for question in Question.objects.all():
        for tag in question.tags.all():
            if tag.title == tag_name:
                tag_questions.append(question)

    page = request.GET.get('page', 1)
    try:
        page = int(page)

    except ValueError:
        return HttpResponseBadRequest()
    tmp = paginate(tag_questions, page)
    return render(request, "index.html", {'questions': tmp, 'page_obj': tmp})


def hot(request):
    page = request.GET.get('page', 1)
    try:
        page = int(page)

    except ValueError:
        return HttpResponseBadRequest()
    questions = Question.objects.hottest()
    tmp = paginate(questions, page)
    return render(request, "index.html", {'questions': tmp, 'page_obj': tmp})

def paginate(objects, page, per_page=5):
    paginator = Paginator(objects, per_page)
    #page_items = paginator.page(1).object_list
    return paginator.page(page)



def index(request):

    page = request.GET.get('page', 1)
    try:
        page = int(page)

    except ValueError:
        return HttpResponseBadRequest()
    #paginator = Paginator(objects, per_page)
    tmp = paginate (Question.objects.newest(), page)
    return render(request, "index.html", {'questions': tmp, 'page_obj': tmp})


def question(request, pk):
    item = Question.objects.id(int(pk)).first()
    if item is None:
        raise Http404
    else:
        answers = item.answers.hottest()
    page = request.GET.get('page', 1)
    try:
        page = int(page)
    except ValueError:
        return HttpResponseBadRequest()
    tmp = paginate(answers, page)
    return render(request, "question.html", {'question': item, 'answers': tmp, 'page_obj': tmp})
    #return render(request, "question.html", {'question': item})


def login(request):
    return render(request, "login.html")

def ask(request):
    return render(request, 'ask.html')


def settings(request):
    return render(request, 'settings.html')

def signup (request):
    return render(request, 'signup.html')

class VotesView(View):
    model = None
    vote_type = None

    def post(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        try:
            like_dislike = Like.objects.get(content_type=ContentType.objects.get_for_model(obj),
                                            object_id=obj.id,
                                            user=request.user)

            if like_dislike.vote is not self.vote_type:
                like_dislike.vote = self.vote_type
                obj.rate += 2*self.vote_type
                obj.author.rank += 2*self.vote_type
                like_dislike.save(update_fields=['vote'])
                result = True
            else:
                obj.rate -= self.vote_type
                like_dislike.delete()
                result = False
        except Like.DoesNotExist:
            obj.votes.create(user=request.user, vote=self.vote_type)
            obj.rate += self.vote_type
            obj.author.rank += self.vote_type
            result = True

        obj.save()
        obj.author.save()
        return HttpResponse(
            json.dumps({
                "result": result,
                "like_count": obj.votes.likes().count(),
                "dislike_count": obj.votes.dislikes().count(),
                "sum_rating": obj.votes.sum_rating()
            }),
            content_type="application/json"
        )