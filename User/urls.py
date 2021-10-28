from django.urls import path
from . import views


urlpatterns = [
    path('add', views.AddPostView.as_view(), name = "add"),
    path('index', views.AllPostsView.as_view(), name = "index"),
    path('login', views.Login.as_view(), name = "login"),
    path('register', views.Register.as_view(), name = "register"),
    path('', views.Home.as_view(), name = "home"),
    path('logout', views.logout, name = "logout"),
]