from django import forms
from django.core.exceptions import ValidationError
from django.forms import ImageField

from .models import *


class LogInForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput)

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Password'}))

    def clean_password(self):
        data = self.cleaned_data['password']
        return data

    class Meta:
        model = User
        fields = ('username', 'password')


class SignUp(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'minlength': 1,
                                                               'maxlength': 40,
                                                               'placeholder': 'First name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'minlength': 1,
                                                              'maxlength': 40,
                                                              'placeholder': 'Last name'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'minlength': 1,
                                                             'maxlength': 30,
                                                             'placeholder': 'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control',
                                                            'placeholder': 'E-mail'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Password'}))
    password_confirmation = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                              'placeholder': 'Password confirmation'}))

    def clean(self):
        password = self.cleaned_data['password']
        password_confirmation = self.cleaned_data['password_confirmation']
        if password != password_confirmation:
            raise ValidationError('Password confirmation failed')

    def clean_username(self):
        new_user_name = self.cleaned_data['username']
        if User.objects.filter(username=new_user_name).exists():
            raise ValidationError('This username already exists')
        return new_user_name

    def clean_email(self):
        new_email = self.cleaned_data['email']
        print(new_email)
        print(User.objects.filter(email=new_email).exists())
        if User.objects.filter(email=new_email).exists():
            raise ValidationError('User with this email already exists')
        return new_email

    def save(self, **kwargs):
        self.cleaned_data.pop('password_confirmation')
        return User.objects.create_user(**self.cleaned_data)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',)


class AskForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                          'placeholder': 'Enter your title',
                                                          'minlength': 1,
                                                          'maxlength': 100}))
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',
                                                        'placeholder': 'Enter your question',
                                                        'minlength': 1,
                                                        'maxlength': 1000}))
    tags = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'Enter your tags',
                                                         'minlength': 1,
                                                         'maxlength': 100}))

    def save(self, author):
        all_tags = self.cleaned_data['tags'].split(', ')
        title = self.cleaned_data['title']
        text = self.cleaned_data['text']
        question = Question.objects.create(author=author,
                                           date=timezone.now(),
                                           title=title,
                                           body=text)
        for tag in all_tags:
            tag_obj = Tag.objects.get_or_create(title=tag)[0]
            question.tags.add(tag_obj)
        return question

    class Meta:
        model = Question
        fields = {'title', 'text', 'tags'}


class AddAnswer(forms.Form):
    ans_text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',
                                                            'placeholder': "Enter your answer",
                                                            'minlength': 1,
                                                            'maxlength': 1000}))

    def save(self, author, question):
        text = self.cleaned_data['ans_text']
        answer = Answer.objects.create(author=author,
                                       date=timezone.now(),
                                       question=question,
                                       text=text)
        answer.save()
        return answer

    class Meta:
        model = Answer
        fields = {'ans_text'}


class SettingsForm(forms.ModelForm):
    Photo = ImageField(required=False)

    def save(self, **kwargs):
        user = super().save(**kwargs)
        received_avatar = self.cleaned_data['Photo']
        if received_avatar:
            user.avatar = self.cleaned_data['Photo']
        user.save()
        return user

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
