from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):



    username = forms.CharField(widget=forms.TextInput(
        attrs={
        'class':'input',
        'placeholder':'CityTownsvilleApartments'
        }
    ))

    email = forms.CharField(widget=forms.TextInput(
        attrs={
        'class':'input',
        'placeholder':'community@email.com'
        }
    ))

    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
        'class':'input',
        'placeholder':'Password1'
        }
    ))

    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
        'class':'input',
        'placeholder':'Password2'
        }
    ))




    class Meta:
        model = User

        fields = ['username', 'email', 'password1', 'password2']
