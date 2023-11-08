from django.utils import timezone

from rest_framework import serializers

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
        )


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
