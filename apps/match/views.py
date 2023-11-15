from django.shortcuts import render

from rest_framework import viewsets

from . import models, serializers


class MatchViewSet(viewsets.ModelViewSet):
    queryset = models.Match.objects.all()
    serializer_class = serializers.MatchModelSerializer


class MatchChatViewSet(viewsets.ModelViewSet):
    queryset = models.MatchChat.objects.all()
    serializer_class = serializers.MatchChatModelSerializer
