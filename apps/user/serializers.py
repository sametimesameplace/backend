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

    class Meta:
        model = models.User
        fields = (
            "username",
            "password",
            "email",
            "date_joined",
        )
