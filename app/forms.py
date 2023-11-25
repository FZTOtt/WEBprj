from django import forms

from .models import User


class LogInForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'maxlength': 50,
                                                             'placeholder': 'Username'}))

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = ('username', 'password')