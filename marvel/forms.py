from django import forms
from django.contrib.auth.forms import AuthenticationForm

from marvel.models import Comics


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя')
    password = forms.PasswordInput()


class ComicsForm(forms.ModelForm):
    class Meta:
        model = Comics
        fields = '__all__'
