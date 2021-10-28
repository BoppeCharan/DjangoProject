from django.db import models

class User(models.Model) :
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=130)


class Post(models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now = True)

