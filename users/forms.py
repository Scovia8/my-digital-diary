from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,  AuthenticationForm
from .models import Profile

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

    class Meta:
        fields = ['username', 'password']

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']