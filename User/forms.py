from django import forms
from django.db.models import fields
from django.forms import models
from .models import User, Post

class LoginForm(forms.ModelForm) :
    class Meta :
        model =  User
        fields = ("email", "password")

class RegistrationForm(forms.ModelForm) :
    class Meta :
        model =  User
        fields = ("first_name", "last_name", "username", "email", "password")


class AddPostForm(forms.ModelForm) :
    class Meta :
        model =  Post
        fields = ("text",)

        labels = {
            "text" : "Post Text"
        }

        error_messages = {
            "text" : {
                "required" : "comment should not be empty",
                "maxlength" : "text length should not exceed 200 characters"
            }
        }
