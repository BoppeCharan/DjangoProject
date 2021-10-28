from django.http.response import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from cryptography.fernet import Fernet

from django.views.generic.base import TemplateView
from .forms import LoginForm, RegistrationForm, AddPostForm
from django.views import View
from .models import User, Post

from Tradex import settings

from django.views.generic import ListView

from django.urls import reverse

class Login(View) :
    def get(self, request) :
        if(request.session.get("logged_in", False)) :
            return HttpResponseRedirect(reverse("home"))
        form = LoginForm()
        return render(request, "User/login.html", {
            "form" : form
        })

    def post(self, request) :
        form = LoginForm(request.POST)
        if(form.is_valid()):
            data = form.cleaned_data
            email = data["email"]
            pswd = data["password"]

            if(len(pswd) > 20) :
                return render(request, "Accounts/login.html", {
                    "form" : form,
                    "message" : "Please enter a password of 20 charactes or less."
                })
            
            try :
                identified_user = User.objects.get(email=email)
            except :
                return render(request, "User/login.html", {
                    "form" : form, 
                    "message" : "user doesn't exist. SignUp for a new account"
                })

            key = settings.ENC_DEC_KEY
            fernet = Fernet(key)

            db_pswd = bytes(identified_user.password, 'utf-8')
            db_retrived_pswd = fernet.decrypt(db_pswd).decode()


            if(pswd == db_retrived_pswd) :
                request.session["user_id"] = identified_user.id
                request.session["logged_in"] = True
                return HttpResponseRedirect(reverse("index"))
            else :
                return render(request, "User/login.html", {
                    "form" : form, 
                    "message" : "Password entered is incorrect"
                })

        else :
            return render(request, "User/login.html", {
                "form" : form,
                "message" : "Enter valid Data"
            })



class Register(View) :
    def get(self, request) :
        if(request.session.get("logged_in", False)) :
            return HttpResponseRedirect(reverse("home"))
        form = RegistrationForm()
        return render(request, "User/register.html", {
            "form" : form
        })

    def post(self, request) :
        form = RegistrationForm(request.POST)
        if(form.is_valid()):
            data = form.cleaned_data
            first_name = data["first_name"]
            last_name = data["last_name"]
            username = data["username"]
            email = data["email"]
            passwd = data["password"]

            if(len(passwd) > 20) :
                return render(request, "User/register.html", {
                    "form" : form,
                    "message" : "maximum length password accepted is 20 characters"
                })


            identified_user = User.objects.filter(email=email)
            if(len(identified_user) == 1) :
                return render(request, "User/register.html", {
                    "form" : form,
                    "message" : "This Email already exists. Please create a new account"
                })

            else :
                key = settings.ENC_DEC_KEY
                fernet = Fernet(key)
                pswd = str(fernet.encrypt(passwd.encode()))[2:-1]

                new_user = User(username = username, password = pswd, email = email, first_name = first_name, last_name = last_name)
                new_user.save()

                return render(request, "User/home.html", {
                    "message" : "Please click on Login to login to your account",
                    "logged_in" : request.session.get("logged_in", False)
                })   

        else :
            return render(request, "User/register.html", {
                "form" : form,
                "message" : "Enter valid Data"
            })

class AllPostsView(View) :
    def get(self, request) :
        if(not request.session.get("logged_in", False)) :
            return HttpResponseRedirect(reverse("home"))

        message = None
        form = AddPostForm()
        all_objects = Post.objects.all()

        return render(request, "User/index.html", {
            "all_objects" : all_objects,
            "logged_in" : request.session.get("logged_in", False),
            "message" : message,
            "form" : form
        })

class AddPostView(View) :

    def post(self, request) :
        form = AddPostForm(request.POST)
        if(form.is_valid()) : 
            data = form.cleaned_data
            text = data["text"]

            user = User.objects.get(pk = request.session.get("user_id"))

            post_object = form.save(commit=False)
            post_object.user = user
            post_object.save()

            return HttpResponseRedirect(reverse("index"))

            
        else :
            return render(request, "User/index.html", {
                "form" : form,
                "logged_in" : request.session.get("logged_in", False)
            })

class Home(View) :
    def get(self, request) :
        if(request.session.get("logged_in", False)) :
            return HttpResponseRedirect(reverse("index"))

        return render(request, "User/home.html", {
            "user_id" : request.session.get("user_id", None),
            "logged_in" : request.session.get("logged_in", False)
        })

def logout(request) :
    request.session["logged_in"] = False
    request.session["user_id"] = None
    return render(request, "User/logout.html")