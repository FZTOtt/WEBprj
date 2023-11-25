"""
URL configuration for askme_zhidkov project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import re_path as url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path
from app.models import *
from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('question/<int:pk>', views.question, name='question'),
    path('login/', views.log_in, name='log_in'),
    path('logout', views.log_out, name='logout'),
    path('ask', views.ask, name='ask'),
    path('settings', views.settings, name='profile_settings'),
    path('signup', views.signup, name='signup'),
    path('admin/', admin.site.urls),
    path('hot', views.hot, name='hot'),
    path('tag/<str:tag_name>', views.tag, name='tag'),
    url(r'^question/(?P<pk>\d+)/like/$',
        login_required(views.VotesView.as_view(model=Question, vote_type=Like.LIKE)),
        name='question_like'),
    url(r'^question/(?P<pk>\d+)/dislike/$',
        login_required(views.VotesView.as_view(model=Question, vote_type=Like.DISLIKE)),
        name='question_dislike'),
    url(r'^answer/(?P<pk>\d+)/like/$',
        login_required(views.VotesView.as_view(model=Answer, vote_type=Like.LIKE)),
        name='answer_like'),
    url(r'^answer/(?P<pk>\d+)/dislike/$',
        login_required(views.VotesView.as_view(model=Answer, vote_type=Like.DISLIKE)),
        name='answer_dislike'),
]
