from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Comment, userInfo, newsCategory

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'})
        }

class CreateUserForm(forms.ModelForm):
    class Meta:
        model = userInfo
        fields = ['dob',]
        widgets = {
        'dob': forms.DateInput(format=('%m/%d/%Y'), attrs={'type':'date', 'class':'form-control'}),
        }
        labels = {
            "dob": "Date of birth"
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body",]
        labels = {
            "body": "Add Comment"
        }
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'})
        }

class ImageForm(forms.ModelForm):
    class Meta:
        model = userInfo
        fields = ['pic',]
        labels = {
            "pic": "Upload profile picture"
        }

class FavoritesForm(forms.ModelForm):
    class Meta:
        model = userInfo
        fields = ['favourites',]
        widgets = {
            'favourites': forms.HiddenInput()
        }