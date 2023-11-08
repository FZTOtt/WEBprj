from django.contrib import admin
from .models import Question, Answer, Tag, Like, User
from django.contrib.auth.admin import UserAdmin
# Register your models here.

# class CustomUserAdmin(UserAdmin):
#     model = customUser
admin.site.register(User, UserAdmin)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Tag)
admin.site.register(Like)

