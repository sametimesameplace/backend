from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from . import models, permissions, serializers


class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class InterestViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.SuperOrReadOnly,)
    pagination_class = StandardPagination

    queryset = (models.Interest.objects.all()
                .order_by("name"))

    serializer_class = serializers.InterestModelSerializer


class ActivityViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.SuperOrReadOnly,)
    pagination_class = StandardPagination

    queryset = (models.Activity.objects.all()
                .order_by("name"))

    serializer_class = serializers.ActivityModelSerializer


class TimePlaceViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedCreateOrSuperOrAuthor,)
    pagination_class = StandardPagination

    queryset = (models.TimePlace.objects.all()
                .select_related("user_id")
                .prefetch_related("interests", "activities")
                .order_by("-created_at"))

    def get_serializer_class(self):
        """Use the CreateUpdateSerializer for create and update
        so interests and activities can be provided with lists of ids
        """
        if self.action in ("create", "update"):
            return serializers.TimePlaceModelCreateUpdateSerializer
        return serializers.TimePlaceModelViewSerializer

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
