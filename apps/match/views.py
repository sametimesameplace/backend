from django.shortcuts import render

from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from . import models, serializers


class MatchViewSet(viewsets.ModelViewSet):
    queryset = models.Match.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.MatchModelSerializer

    @action(detail=True, methods=["GET"], url_path="chat")
    def chat(self, request, *args, **kwargs):
        match = models.MatchChat.objects.filter(match_id=self.get_object().id)
        serializer = serializers.MatchChatModelSerializer(data=request.data)
        if serializer.is_valid():
            match.chat(serializer.validated_data["message"])
            match.save()
            return Response("success", status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
