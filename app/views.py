from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import AnonymousUser
from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseBadRequest, HttpResponse
from django.urls import reverse
from django.views import View
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect

from .forms import *
from .models import *
from django.http import Http404




def tag(request, tag_name):
    question = Question.objects.all()
    question = question.filter(tags__title=tag_name)

    tmp = paginate(question, request)
    return render(request, "index.html", {'questions': tmp, 'page_obj': tmp})


def hot(request):
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

@login_required(login_url='log_in')
def profile(request, username):
    user = User.objects.by_username(username)
    if user is not None:
        return render(request, 'profile.html', {'profile': user})


def index(request):

    tmp = paginate(Question.objects.newest(), request)
    if tmp == HttpResponseBadRequest():
        raise Http404
    return render(request, "index.html", {'questions': tmp, 'page_obj': tmp})


# @login_required(login_url='log_in', redirect_field_name='continue')
# def add_answer(request, pk, text):
#     print('ADD')
#     answer = Answer.objects.create(author=request.user,
#                                    date=timezone.now(),
#                                    question=Question.objects.id(pk).first(),
#                                    text=text)
#     answer.save()
#     return redirect(request.GET.get('continue', '/'))

def question(request, pk):
    item = Question.objects.id(int(pk)).first()
    print(item)
    if item is None:
        raise Http404
    else:
        answers = item.answers.all()

    print('paginate')
    if request.method == 'GET':
        print('get')
        answer_form = AddAnswer()
    if request.method == 'POST':
        print('post')
        answer_form = AddAnswer(request.POST)
        if answer_form.is_valid():
            if not request.user.is_authenticated:
                return redirect('log_in')
            else:
                answer_form.save(request.user, item)
                answers = item.answers.all()
                return redirect('question', pk)
    tmp = paginate(answers, request)
    return render(request, 'question.html', {'question': item,
                                                 'answers': tmp,
                                                 'page_obj': tmp,
                                                 'form': answer_form})
    # return render(request, "question.html", {'question': item, 'answers': tmp, 'page_obj': tmp})
    # return render(request, "question.html", {'question': item})


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
            print(user)

            if user is not None:
                login(request, user)
                print('success')
                return redirect(request.GET.get('continue', '/'))
            else:
                login_form.add_error(None, "User doesn't exist or wrong password")
    return render(request, "login.html", context={"form": login_form})


@login_required(login_url='log_in', redirect_field_name='continue')
def log_out(request):
    if not request.user.is_authenticated:
        raise Http404
    logout(request)
    return redirect(reverse('index'))


@login_required(login_url='log_in', redirect_field_name='continue')
def ask(request):
    if request.method == 'GET':
        question_form = AskForm()
    if request.method == 'POST':
        print("POST")
        question_form = AskForm(request.POST)
        if question_form.is_valid():
            question = question_form.save(request.user)
            print(question.pk)
            return redirect('question', question.pk)

        # else:
            # question_form.add_error(None, "Question saving error")
            # question_form.add_error('title', "Max length of title is 100 symbols")
            # question_form.add_error('body', "Max length of text is 1000 symbols")
            # question_form.add_error('tags', "Add tags")
            # user_form.add_error("username", "")
            # user_form.add_error("password", "")
    return render(request, "ask.html", context={"form": question_form})

@csrf_protect
@login_required(login_url='log_in', redirect_field_name='continue')
def settings(request):
    if request.method == "GET":
        form = SettingsForm(initial=model_to_dict(request.user))

    elif request.method == "POST":
        form = SettingsForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            print('valid')
            form.save()
        else:
            form = SettingsForm()
    return render(request, 'settings.html', context={'form': form})

@csrf_protect
def signup(request):
    print(request.GET)
    print(request.POST)
    if request.method == 'GET':
        user_form = SignUp()
    if request.method == 'POST':
        print("POST")
        user_form = SignUp(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            print(user)

            if user:
                login(request, user)
                print('success')
                return redirect(reverse('index'))
    return render(request, "signup.html", context={"form": user_form})

@csrf_protect
@login_required
def correct(request):
    print('correct')
    user = request.user
    id = request.POST.get('id')
    answer = Answer.objects.get(pk=id)
    print(answer.author)
    if Answer.objects.get(pk=id).question.author == user:
        print('true')
        print(Answer.objects.get(pk=id).status)
        Answer.objects.get(pk=id).toggle_status()



    return JsonResponse({
        'chacked': Answer.objects.get(pk=id).status
    })

@csrf_protect
@login_required
def like(request):
    id = request.POST.get('id')
    print (id)
    type = request.POST.get('type')
    if type == 'question':
        obj = Question.objects.get(pk=id)
        content = 8
    else:
        obj = Answer.objects.get(pk=id)
        content = 9
    mark = request.POST.get('mark')
    if mark == '1':
        vote = 1
    else:
        vote = -1
    like = Like()
    like.user = request.user
    like.vote = vote
    like.content_object = obj
    if Like.objects.filter(user_id=like.user.pk, content_type_id=content, object_id=obj.pk).exists():
        Like.objects.filter(user_id=like.user.pk, content_type_id=content, object_id=obj.pk).delete()
    else:
        like.save()

    # "like_count": question.votes.likes().count()

    return JsonResponse({
        'count': obj.votes.sum_rating()
    })
class VotesView(View):
    model = None
    vote_type = None

    def post(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        # try:
        #     like_dislike = Like.objects.get(content_type=ContentType.objects.get_for_model(obj),
        #                                     object_id=obj.id,
        #                                     user=request.user)
        #
        #     if like_dislike.vote is not self.vote_type:
        #         like_dislike.vote = self.vote_type
        #         obj.rating += self.vote_type
        #         obj.author.rating += self.vote_type
        #         like_dislike.save(update_fields=['vote'])
        #         result = True
        #     else:
        #         obj.rate -= self.vote_type
        #         like_dislike.delete()
        #         result = False
        # except Like.DoesNotExist:
        #     obj.votes.create(user=request.user, vote=self.vote_type)
        #     obj.rate += self.vote_type
        #     obj.author.rank += self.vote_type
        #     result = True
        #
        # obj.save()
        # obj.author.save()
        return HttpResponse(
            json.dumps({
                # "result": result,
                "like_count": obj.votes.likes().count(),
                "dislike_count": obj.votes.dislikes().count(),
                "sum_rating": obj.votes.sum_rating()
            }),
            content_type="application/json"
        )
