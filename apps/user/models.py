from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    title = models.CharField(max_length=100, null=True,
                             blank=True, help_text="Your profession")
    bio = models.TextField(default='', blank=True)

    mfa_secret = models.CharField(max_length=255, default='')
    date_joined =  models.DateField(default=timezone.now)


class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    hometown = models.CharField(max_length=255)
    slogan = models.CharField(max_length=255)
    birthday = models.DateField()
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=20)
    profile_email = models.EmailField()


class Language(models.Model):
    id = models.AutoField(primary_key=True)
    lang = models.CharField(max_length=255)
    
    def __str__(self):
        return self.lang

class UserLanguage(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    level_choices = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]
    level = models.CharField(max_length=20, choices=level_choices)

    def __str__(self):
        return f"{self.userprofile} - {self.language} - {self.level}"
