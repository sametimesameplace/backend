from django.utils import timezone

from rest_framework import serializers

from datetime import date

from . import models

from .models import UserProfile


class UserModelSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = models.User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data["email"],
        )

        return user

    def validate_phone(self, value):
        pass

    def validate_email(self, value):
        pass

    class Meta:
        model = models.User
        fields = (
            "id",
            "username",
            "password",
            "email",
            "date_joined",
            "bio",
            "title"
        )

class LanguageModelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Language
        fields = ('id', 'lang')

class UserLanguageModelSerializer(serializers.ModelSerializer):
    # language = LanguageModelSerializer()
    
    class Meta:
        model = models.UserLanguage
        fields = ('id', 'userprofile', 'language', 'level')

class UserProfileModelSerializer(serializers.ModelSerializer):
    user = UserModelSerializer()
    languages = UserLanguageModelSerializer(many=True, source='user_language')
    age = serializers.SerializerMethodField()

    class Meta:
        model = models.UserProfile
        fields = (
            'id', 'user', 'name', 'hometown', 'slogan', 'birthday',
            'gender', 'phone', 'profile_email', 'languages', 'age'
        )

    def get_age(self, obj):
        today = date.today()
        birthdate = obj.birthday
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        return age
    

class UserProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            "user",
            "name",
            "hometown",
            "slogan",
            "birthday",
            "gender",
            "phone",
            "profile_email",
            "languages"
        )

        # def validate_birthday(self, birthday):
        #     # Check if the birthday is in past (or age < 18)
        #     if birthday > timezone.now().date():
        #         raise serializers.ValidationError("Invalid birthday")
        #     return birthday


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    # Birthday cannot be updated
    class Meta:
        model = UserProfile
        fields = (
            "user",
            "name",
            "hometown",
            "slogan",
            "gender",
            "phone",
            "profile_email",
            "languages"
        )


class UserProfileRetrieveSerializer(serializers.ModelSerializer):
    # Returns age instead of birthday
    class Meta:
        model = UserProfile
        fields = (
            "user",
            "name",
            "hometown",
            "slogan",
            "age",
            "gender",
            "phone",
            "profile_email",
            "languages"
        )
