from datetime import datetime, timezone

from django.db.models import Q

from rest_framework import status
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiResponse

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
            return models.Match.objects.all().order_by("-created_at")
        return (models.Match.objects
                .exclude(deleted=True)
                .filter(Q(timeplace_1__user=self.request.user) |
                        Q(timeplace_2__user=self.request.user))
                .order_by("-created_at")
                )
    
    def perform_destroy(self, instance):
        """Don't delete the instance but rather set 'deleted' to true
        and deleted_on to the current timestamp.
        """
        instance.deleted = True
        instance.deleted_on = datetime.now(tz=timezone.utc)
        instance.save()

    @extend_schema(
        request=None,
        responses={
            201: OpenApiResponse(),
            403: OpenApiResponse(),
            }
        )
    @action(detail=True, methods=["POST"], url_path="share_email")
    def share_email(self, request, pk=None):
        """Set the email_user_x field to True for the user of the request.
        """
        obj = self.get_object()
        success = False
        if obj.timeplace_1.user == self.request.user:
            if obj.email_user_1:
                pass
            else:
                obj.email_user_1=True
                obj.save()
                success = True
        elif obj.timeplace_2.user == self.request.user:
            if obj.email_user_2:
                pass
            else:
                obj.email_user_2=True
                obj.save()
                success = True
        if success:
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    @extend_schema(
        request=None,
        responses={
            201: OpenApiResponse(), 
            403: OpenApiResponse(),
            }
        )
    @action(detail=True, methods=["POST"], url_path="share_phone")
    def share_phone(self, request, pk=None):
        """Set the phone_user_x field to True for the user of the request.
        """
        obj = self.get_object()
        success = False
        if obj.timeplace_1.user == self.request.user:
            if obj.phone_user_1:
                pass
            else:
                obj.phone_user_1=True
                obj.save()
                success = True
        elif obj.timeplace_2.user == self.request.user:
            if obj.phone_user_2:
                pass
            else:
                obj.phone_user_2=True
                obj.save()
                success = True
        if success:
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

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
