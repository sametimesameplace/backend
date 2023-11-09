from django.utils import timezone

from rest_framework import serializers

from . import models


class UserModelSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = models.User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data["email"],
        )

        return user

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
        model = models.UserProfile
        fields = (
            "name",
            "hometown",
            "slogan",
            "birthday",
            "gender",
            "phone",
            "profile_email",
        )

        def validate_phone(self, phone):
            pass

        def validate_birthday(self, birthday):
            pass
       


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    # Birthday cannot be updated
    class Meta:
        model = models.UserProfile
        fields = (
            "name",
            "hometown",
            "slogan",
            "gender",
            "phone",
            "profile_email",
        )


class UserProfileRetrieveSerializer(serializers.ModelSerializer):
    # Returns age instead of birthday
    class Meta:
        model = models.UserProfile
        fields = (
            "user",
            "name",
            "hometown",
            "slogan",
            "age",
            "gender",
            "phone",
            "profile_email",
        )
