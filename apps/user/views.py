from django.contrib.auth import authenticate

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated

from . import serializers
from .models import User, UserProfile, UserLanguage, Language
# from .serializers import UserModelSerializer, UserProfileModelSerializer, UserProfileUpdateSerializer, UserProfileCreateSerializer, UserLoginSerializer, UserLanguageModelSerializer
from .permissions import UserSuperDeleteOnly
from apps.timeplace.permissions import IsAuthenticatedCreateOrSuperOrAuthor, SuperOrReadOnly


class UserLoginView(viewsets.ModelViewSet):
    """handle user login functionality, the associated model for this view represents user data from the authentication fields"""
        
    serializer_class = serializers.UserLoginSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """validating the incoming data, authenticating the user based on the provided credentials, and generating a token for the authenticated user. """
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(
            username=username,
            password=password,
        )
        if not user:
            return Response(
                {"error": "Password or Username incorrect"},
                status=status.HTTP_403_FORBIDDEN
            )

        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {"token": token.key},
            status=status.HTTP_200_OK
        )


class ListUsers(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserModelSerializer
    permission_classes = [UserSuperDeleteOnly]
    def get_permissions(self):
        """Unauthenticated users should be able to create a user.
        """
        if self.action == "create":
            return [AllowAny()]
        else:
            return [UserSuperDeleteOnly()]

    def get_queryset(self):
        """Filter objects so a user only sees themself.
        If user is admin, let them see all.
        """
        if self.request.user.is_staff:
            return User.objects.all()
        else:
            return User.objects.filter(id=self.request.user.id)


class UserProfileModelViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    permission_classes = (
        IsAuthenticatedCreateOrSuperOrAuthor,
    )

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.UserProfileCreateSerializer
        elif self.action == "update":
            return serializers.UserProfileUpdateSerializer
        return serializers.UserProfileModelSerializer

    def perform_create(self, serializer):
        """The logged in user is always the author
        """
        return serializer.save(user_id=self.request.user)

    def get_queryset(self):
        """Limit the queryset to the author, 
        i.e the logged in user, for fetching/updating data
        """
        if self.request.user.is_superuser:
            return self.queryset
        return self.queryset.filter(user_id=self.request.user)


class UserLanguageViewSet(viewsets.ModelViewSet):
    queryset = UserLanguage.objects.all()
    serializer_class = serializers.UserLanguageModelSerializer  
    permission_classes = [IsAuthenticated] 
    
    def get_queryset(self):
        """Filter objects so a user only his UserLanguage.
        If user is admin, let them see all.
        """
        if self.request.user.is_superuser:
            return UserLanguage.objects.all()
        else:
            return UserLanguage.objects.filter(userprofile__user=self.request.user)


class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = serializers.LanguageModelSerializer  
    permission_classes = [SuperOrReadOnly] 
