from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm,widgets
from django import forms
from django.contrib.auth.models import User
from django.core.files.images import get_image_dimensions

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email','username','password1','password2']