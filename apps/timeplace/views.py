from datetime import datetime, timezone
from decimal import Decimal

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from geopy.distance import distance

from . import models, permissions, serializers


class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class InterestViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.SuperOrReadOnly,)
    pagination_class = StandardPagination

    queryset = models.Interest.objects.all().order_by("name")

    serializer_class = serializers.InterestModelSerializer


class ActivityViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.SuperOrReadOnly,)
    pagination_class = StandardPagination

    queryset = models.Activity.objects.all().order_by("name")

    serializer_class = serializers.ActivityModelSerializer


class TimePlaceViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedCreateOrSuperOrAuthor,)
    pagination_class = StandardPagination

    queryset = (
        models.TimePlace.objects.all()
        .select_related("user")
        .prefetch_related("interests", "activities")
        .order_by("-created_at")
    )

    def get_serializer_class(self):
        """Use the CreateUpdateSerializer for create and update
        so interests and activities can be provided with lists of ids
        """
        if self.request.user.is_superuser:
            return serializers.TimePlaceModelAdminSerializer
        elif self.action in ("create", "update"):
            return serializers.TimePlaceModelCreateUpdateSerializer
        return serializers.TimePlaceModelViewSerializer

    def perform_create(self, serializer):
        """The logged in user is always the author
        """
        return serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        """Don't delete the instance but rather set 'deleted' to true
        and deleted_on to the current timestamp.
        """
        instance.deleted = True
        instance.deleted_on = datetime.now(tz=timezone.utc)
        instance.save()

    def get_queryset(self):
        """Limit the queryset to the author, i.e the logged in user, 
        and non-deleted items for fetching/updating data.
        Superusers can see all items.
        """
        if self.request.user.is_superuser:
            return self.queryset
        return self.queryset.filter(user=self.request.user).filter(deleted=False)

    def check_match(self, main_tp, check_tp):
        """Checks if two timeplaces are a match.

        Args:
            main_tp (TimePlace): The main timeplace to check against.
            check_tp (TimePlace): The potential match to check.

        Returns:
            bool: True if match, False if not.
        """
        # Check if the distance between the timeplaces is within the smallest radius
        radius = min(main_tp.radius, check_tp.radius)
        if radius < distance((main_tp.latitude, main_tp.longitude),
                             (check_tp.latitude, check_tp.longitude)).km:
            return False
        # Check if there is at least one overlapping interest
        if not main_tp.interests.all().intersection(check_tp.interests.all()):
            return False
        # Check if there is at least one overlapping activity
        if not main_tp.activities.all().intersection(check_tp.activities.all()):
            return False
        return True

    @action(detail=True, methods=["GET"], url_path="matches")
    def matches(self, request, *args, **kwargs):
        """View all potential matches of a Timeplace
        """
        # the TimePlace this view belongs to
        obj = self.get_object()
        # get the list of language ids to filter the queryset with
        obj_langs = [lang[0] for lang in obj.user.userprofile.languages.values_list()]


        # get all timeplaces with overlapping timeframe and lat/long 
        queryset = (models.TimePlace.objects
                    .select_related("user", "user__userprofile")
                    .prefetch_related("interests", "activities", 
                                      "user__userprofile__languages")
                    .all()
                    .filter(
                        # filter start and end time to be less/greater than obj
                        start__lte = obj.end,
                        end__gte = obj.start,
                        # .1° is about 11km, so dividing the radius by 100
                        latitude__lte = obj.latitude + Decimal(obj.radius/100),
                        latitude__gte = obj.latitude - Decimal(obj.radius/100),
                        longitude__lte = obj.longitude + Decimal(obj.radius/100),
                        longitude__gte = obj.longitude - Decimal(obj.radius/100),
                        user__userprofile__languages__id__in = obj_langs,
                    )
                    # excludes results by the same user
                    .exclude(user=obj.user)
                    .order_by("start")
                )
        # Check each potential match for distance, interests and activities
        non_matches = []
        for tp in queryset:
            if not self.check_match(obj, tp):
                non_matches.append(tp.id)
        # Exclude the results that don't match
        queryset = queryset.exclude(id__in=non_matches)
        

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializers.TimePlaceMatchSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializers.TimePlaceMatchSerializer(queryset, many=True)
        return Response(serializer.data)
