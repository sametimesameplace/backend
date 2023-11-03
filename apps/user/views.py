from typing import Optional

from django.contrib.auth import authenticate

from rest_framework import status  
from rest_framework.views import APIView  
from rest_framework.response import Response  
from rest_framework.authtoken.models import Token 

from .models import User


class UserLoginView(APIView):
    def post(self, request):
        # get credentials
        password = request.data.get('password')
        username = request.data.get('username')

        # authenticate the user
        user: Optional[User] = authenticate(
            username = username,
            password = password,
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