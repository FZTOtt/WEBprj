from django import forms
from django.core.exceptions import ValidationError

from .models import User


class LogInForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput)

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Password'}))

    def clean_password(self):
        data = self.cleaned_data['password']
        if data == 'wrong':
            raise ValidationError("wrong password")
        return data
    class Meta:
        model = User
        fields = ('username', 'password')


class SignIn(forms.ModelForm):
    first_name = forms.CharField(validators=[textValidator],
                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'minlength': 2,
                                                               'maxlength': 50,
                                                               'placeholder': 'First name'}))
    last_name = forms.CharField(validators=[textValidator],
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'minlength': 2,
                                                              'maxlength': 50,
                                                              'placeholder': 'Last name'}))
    username = forms.CharField(validators=[textValidator],
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'minlength': 4,
                                                             'maxlength': 50,
                                                             'placeholder': 'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control',
                                                            'placeholder': 'E-mail'}))
    password = forms.CharField(validators=[passwordValidator],
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Password'}))
    password_confirmation = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                              'placeholder': 'Password confirmation'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',)