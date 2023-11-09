from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponseBadRequest
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
