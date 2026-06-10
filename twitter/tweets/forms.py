from django import forms
from django.contrib.auth.models import User #importing django built in user model 
from django.contrib.auth.forms import UserCreationForm # UserCreationForm is a ready made form provided by the django
from .models import Tweet

class RegistrationForm(UserCreationForm): #inheriting the ready made form
    class Meta: # this provides settings or configurations for this form 
        model = User #save data in the user table
        fields = ['username'] #include username in the form, password is already given by the usercreationform

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content', 'image']