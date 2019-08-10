from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    username = forms.CharField(max_length=20)
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput())
    typeuser = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1','typeuser')


class Edit(UserCreationForm):
    typeuser = forms.CharField(max_length=20)


class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')
        #exclude =('password1','typeuser')