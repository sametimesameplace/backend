from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(("email address"), unique=True)
    title = models.CharField(max_length=100, null=True,
                             blank=True, help_text="Your profession")
    bio = models.TextField(default='', blank=True)


class Language(models.Model):
    lang = models.CharField(max_length=255)

    def __str__(self):
        return self.lang


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    hometown = models.CharField(max_length=255)
    slogan = models.CharField(max_length=255)
    birthday = models.DateField()
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('D', 'Diverse'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=20)
    profile_email = models.EmailField()
    languages = models.ManyToManyField("user.Language", through="UserLanguage")


class UserLanguage(models.Model):
    userprofile = models.ForeignKey(UserProfile, related_name="user_language", on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    level_choices = [
        ('Learning', 'Learning'),
        ('Fluent', 'Fluent'),
        ('Preferred', 'Preferred'),
    ]
    level = models.CharField(max_length=20, choices=level_choices)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['userprofile', 'language'], name='unique language')
        ]

    def __str__(self):
        return f"{self.userprofile} - {self.language} - {self.level}"
