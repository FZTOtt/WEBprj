from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseBadRequest, HttpResponse
from django.urls import reverse
from django.views import View
import json

from django.views.decorators.csrf import csrf_protect

from .forms import LogInForm
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
    question = Question.objects.all()
    question = question.filter(tags__title=tag_name)
    # for question in Question.objects.all():
    #     for tag in question.tags.all():
    #         if tag.title == tag_name:
    #             tag_questions.append(question)


    tmp = paginate(question, request)
    return render(request, "index.html", {'questions': tmp, 'page_obj': tmp})


def hot(request):
    page = request.GET.get('page', 1)
    questions = Question.objects.hottest()
    tmp = paginate(questions, request)
    if tmp == HttpResponseBadRequest():
        raise Http404
    return render(request, "index.html", {'questions': tmp, 'page_obj': tmp})


# objects, request, per_page
def paginate(objects, request, per_page=5):
    paginator = Paginator(objects, per_page)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    return page_obj
    # paginator = Paginator(objects, per_page)
    #page_items = paginator.page(1).object_list
    # return paginator.page(page)



def index(request):

    page = request.GET.get('page', 1)
    #paginator = Paginator(objects, per_page)
    tmp = paginate (Question.objects.newest(), request)
    if tmp == HttpResponseBadRequest():
        raise Http404
    return render(request, "index.html", {'questions': tmp, 'page_obj': tmp})


def question(request, pk):
    item = Question.objects.id(int(pk)).first()
    if item is None:
        raise Http404
    else:
        answers = item.answers.hottest()
    tmp = paginate(answers, request)
    return render(request, "question.html", {'question': item, 'answers': tmp, 'page_obj': tmp})
    #return render(request, "question.html", {'question': item})


@csrf_protect
def log_in(request):
    print(request.GET)
    print(request.POST)
    if request.method == 'GET':
        login_form = LogInForm()
    if request.method == 'POST':
        print("POST")
        login_form = LogInForm(request.POST)
        if login_form.is_valid():
            user = authenticate(request, **login_form.cleaned_data)
            print (user)

            if user is not None:
                login(request, user)
                print('success')
                return redirect(request.GET.get('continue', '/'))
            else:
                login_form.add_error(None, "User doesn't exist or wrong password")
                login_form.add_error("username","")
                login_form.add_error("password", "")
    return render(request, "login.html", context={"form": login_form})

@login_required(login_url='login/', redirect_field_name='continue')
def log_out(request):
    if not request.user.is_authenticated:
        raise Http404
    logout(request)
    return redirect(reverse('index'))

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