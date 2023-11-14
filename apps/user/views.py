from typing import Optional

from django.contrib.auth import authenticate

from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

from .models import User, UserProfile
from .serializers import UserModelSerializer, UserProfileModelSerializer, UserProfileUpdateSerializer, UserProfileCreateSerializer, UserLoginSerializer
from .permissions import UserSuperDeleteOnly
from apps.timeplace.permissions import IsAuthenticatedCreateOrSuperOrAuthor


class UserLoginView(viewsets.ModelViewSet):
    """handle user login functionality, the associated model for this view represents user data from the authentication fields"""
        
    serializer_class = UserLoginSerializer
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
    serializer_class = UserModelSerializer
    permission_classes = [
        UserSuperDeleteOnly,
    ]


class UserProfileModelViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    permission_classes = (
        IsAuthenticatedCreateOrSuperOrAuthor,
    )

    def get_serializer_class(self):
        if self.action == "create":
            return UserProfileCreateSerializer
        elif self.action == "update":
            return UserProfileUpdateSerializer
        return UserProfileModelSerializer

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
