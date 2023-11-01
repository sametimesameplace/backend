from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from . import models, permissions, serializers


class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class InterestViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.SuperOrReadOnly,)
    pagination_class = StandardPagination
    
    queryset = (models.Interest.objects.all()
                .order_by('-id'))

    serializer_class = serializers.InterestModelSerializer


class ActivityViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.SuperOrReadOnly,)
    pagination_class = StandardPagination
    
    queryset = (models.Activity.objects.all()
                .order_by('-id'))

    serializer_class = serializers.ActivityModelSerializer
