from rest_framework import viewsets

from .models import User
from .serializers import UserModelSerializer
from .permissions import UserSuperDeleteOnly


class ListUsers(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = [
        UserSuperDeleteOnly,
    ]
