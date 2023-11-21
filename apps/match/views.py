from datetime import datetime, timezone

from django.shortcuts import render
from django.db.models import Q

from rest_framework import status
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from . import models, serializers, permissions


class MatchViewSet(
                mixins.RetrieveModelMixin,
                mixins.DestroyModelMixin,
                mixins.ListModelMixin,
                viewsets.GenericViewSet):
    """ 
    API endpoint that allows matches to be viewed or edited.
    """
    queryset = models.Match.objects.all()
    permission_classes = [permissions.SuperOrAuthors]
    serializer_class = serializers.MatchModelListRetrieveSerializer

    def get_queryset(self):
        """Limit the queryset to the author, i.e the logged in user, 
        and non-deleted items for fetching/updating data. Superusers can see all items."""
        if self.request.user.is_superuser:
            return models.Match.objects.all()
        return (models.Match.objects
                .exclude(deleted=True)
                .filter(Q(timeplace_1__user=self.request.user) | Q(timeplace_2__user=self.request.user)))
    
    def perform_destroy(self, instance):
        """Don't delete the instance but rather set 'deleted' to true
        and deleted_on to the current timestamp.
        """
        instance.deleted = True
        instance.deleted_on = datetime.now(tz=timezone.utc)
        instance.save()
    
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
