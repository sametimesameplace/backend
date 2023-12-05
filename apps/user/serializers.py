from rest_framework import serializers

from datetime import date

from . import models


class UserModelSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = models.User.objects.create_user(
            username=validated_data["username"].lower(),
            password=validated_data["password"],
            email=validated_data["email"].lower(),
        )

        return user

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
    language = serializers.StringRelatedField()

    class Meta:
        model = models.UserLanguage
        fields = ('id', 'userprofile', 'language', 'level')


class UserLanguageCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UserLanguage
        fields = ('id', 'language', 'level')


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

    def get_age(self, obj) -> int:
        today = date.today()
        birthdate = obj.birthday
        age = today.year - birthdate.year - \
            ((today.month, today.day) < (birthdate.month, birthdate.day))
        return age


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

        def validate_age18plus(self, birthday):
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

class UserLoginSerializer(serializers.Serializer):
    """ ensures that both the username and password fields are present in the input data"""
    
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username, password = data.get('username'), data.get('password')
        if not (username and password):
            raise serializers.ValidationError("Username and password are required.")
        return data