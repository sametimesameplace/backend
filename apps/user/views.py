from typing import Optional

from django.contrib.auth import authenticate

from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import User, UserProfile
from .serializers import UserModelSerializer, UserProfileModelSerializer, UserProfileUpdateSerializer, 
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
    permission_classes = [
        UserSuperDeleteOnly,
    ]


class DisplayUserProfile(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileModelSerializer
    permission_classes = [
        IsAuthenticatedCreateOrSuperOrAuthor,
    ]


class UserProfileUpdateView(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [IsAuthenticatedCreateOrSuperOrAuthor]

    # def get_object(self):
    #     return self.request.user.userprofile
