from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    title = models.CharField(
        max_length=100, null=True, blank=True, help_text="Your profession"
    )
    bio = models.TextField(default="", blank=True)
    username = (models.CharField(max_length=100),)
    password = (models.CharField(max_length=100),)
    email = (models.CharField(max_length=100),)
    mfa_secret = (models.CharField(max_length=100),)
    date_joined = models.DateTimeField(auto_now_add=True)
