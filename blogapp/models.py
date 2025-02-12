# blog/models.py
from django.db import models
from django.contrib.auth.models import User,AbstractUser
import datetime
from django.utils.timezone import timezone 


class datauser(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    qualification = models.CharField(max_length=50, null=False, blank=False, default="12")
    age =  models.IntegerField(null=False, blank=False)
    created = models.DateTimeField(default=datetime.datetime.now())


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.title 
