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
ANSWERS = [
        {
        'id': i,
        'title': f'Answer {i}',
        'content': f'Let me help you {i}'
    } for i in range (20)
    ]


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
    return render(request, "index.html", {'questions': tmp, 'page_obj' : tmp})


def question(request, pk):
    item = Question.objects.id(int(pk)).first()
    if item is None:
        raise Http404
    page = request.GET.get('page', 1)
    try:
        page = int(page)
    except ValueError:
        return HttpResponseBadRequest()
    tmp = paginate(ANSWERS, page)
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
