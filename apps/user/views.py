from typing import Optional

from django.contrib.auth import authenticate

from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

from .models import User, UserProfile
from .serializers import UserModelSerializer, UserProfileModelSerializer, UserProfileUpdateSerializer, UserProfileCreateSerializer
from .permissions import UserSuperDeleteOnly
from apps.timeplace.permissions import IsAuthenticatedCreateOrSuperOrAuthor


class UserLoginView(APIView):
    def post(self, request):
        # get credentials
        password = request.data.get('password')
        username = request.data.get('username')

        # authenticate the user
        user: Optional[User] = authenticate(
            username=username,
            password=password,
        )
        if not user:
            return Response(
                {"error": "Password or Username incorrect"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Create the token
        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {"token": token.key},
            status=status.HTTP_200_OK
        )


class ListUsers(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
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
