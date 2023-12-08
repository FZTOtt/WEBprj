from django.urls import re_path as url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path
from .models import *
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('question/<int:pk>', question, name='question'),
    path('login/', log_in, name='log_in'),
    path('logout', log_out, name='logout'),
    path('ask', ask, name='ask'),
    path('settings', settings, name='profile_settings'),
    path('signup', signup, name='signup'),
    path('admin/', admin.site.urls),
    path('hot', hot, name='hot'),
    path('tag/<str:tag_name>', tag, name='tag'),
    path('like/', like, name='like'),
    path('correct/', correct, name='correct'),
    url(r'^question/(?P<pk>\d+)/like/$',
        login_required(VotesView.as_view(model=Question, vote_type=Like.LIKE)),
        name='question_like'),
    url(r'^question/(?P<pk>\d+)/dislike/$',
        login_required(VotesView.as_view(model=Question, vote_type=Like.DISLIKE)),
        name='question_dislike'),
    url(r'^answer/(?P<pk>\d+)/like/$',
        login_required(VotesView.as_view(model=Answer, vote_type=Like.LIKE)),
        name='answer_like'),
    url(r'^answer/(?P<pk>\d+)/dislike/$',
        login_required(VotesView.as_view(model=Answer, vote_type=Like.DISLIKE)),
        name='answer_dislike'),
]
