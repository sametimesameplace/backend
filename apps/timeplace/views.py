from datetime import datetime, timezone
from decimal import Decimal

from django.db.models import Q
from rest_framework import viewsets
from rest_framework import status
from rest_framework import serializers as drf_serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from geopy.distance import distance
from drf_spectacular.utils import extend_schema, extend_schema_view, inline_serializer
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, OpenApiResponse

from apps.match.models import Match
from apps.match.serializers import MatchModelListRetrieveSerializer
from . import models, permissions, serializers


class InterestViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.SuperOrReadOnly,)

    queryset = models.Interest.objects.all().order_by("name")

    serializer_class = serializers.InterestModelSerializer


class ActivityViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.SuperOrReadOnly,)

    queryset = models.Activity.objects.all().order_by("name")

    serializer_class = serializers.ActivityModelSerializer


@extend_schema_view(
    create=extend_schema(
        description="""Create a new TimePlace.
        Latitude and Longitude are numbers with up to six decimal places.
        Latitude needs to be between -90 and 90.
        Longitude needs to be between -180 and 180.""",
        request=serializers.TimePlaceModelCreateSerializer,
        responses={201: serializers.TimePlaceModelViewSerializer}))
class TimePlaceViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedCreateOrSuperOrAuthor,)

    queryset = (
        models.TimePlace.objects.all()
        .select_related("user")
        .prefetch_related("interests", "activities")
        .order_by("-created_at")
    )

    def get_serializer_class(self):
        """Use the CreateSerializer for create and the UpdateSerializer for 
        update so interests and activities can be provided with lists of ids
        """
        if self.request.user.is_superuser:
            return serializers.TimePlaceModelAdminSerializer
        elif self.action == "create":
            return serializers.TimePlaceModelCreateSerializer
        elif self.action == "update":
            return serializers.TimePlaceModelUpdateSerializer
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
    
    @extend_schema(responses=serializers.TimePlaceMatchSerializer(many=True))
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
                    # excludes results by the same user
                    .exclude(user=obj.user)
                    .exclude(deleted=True)
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
                    .distinct()
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

    @extend_schema(
        parameters=[OpenApiParameter("timeplace_pk",
                    OpenApiTypes.INT,
                    OpenApiParameter.PATH),],
        responses={
            200: inline_serializer(
                name='get_match_response',
                fields={
                    'match_id': drf_serializers.IntegerField(),
                }
            )
            }
        )
    @action(detail=True, methods=["GET"], url_path="match/(?P<timeplace_pk>[^/.]+)")
    def get_match(self, request, timeplace_pk: int, pk=None):
        """Check if there is an existing match object between two timeplaces.
        """
        
        own_tp = self.get_object().id
        other_tp = timeplace_pk

        queryset = (Match.objects.filter(
            (Q(timeplace_1_id=own_tp) | Q(timeplace_1_id=other_tp)) &
            (Q(timeplace_2_id=own_tp) | Q(timeplace_2_id=other_tp))
        )
        .order_by("-created_at"))

        if queryset:
            return Response(
                {"match_id": queryset[0].id},
                status=status.HTTP_200_OK
                )
        return Response(status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        parameters=[OpenApiParameter("timeplace_pk",
                    OpenApiTypes.INT,
                    OpenApiParameter.PATH),],
        request=None,
        responses={
            201: inline_serializer(
                name='create_match_response',
                fields={
                    'match_id': drf_serializers.IntegerField(),
                }
            ), 
            403: OpenApiResponse(description='Match already exists'),
            }
        )
    @get_match.mapping.post
    def create_match(self, request, timeplace_pk: int, pk=None):
        """Create a new match object for two timeplaces.
        """
        own_tp = self.get_object()
        other_tp = models.TimePlace.objects.get(pk=timeplace_pk)

        if own_tp.user == other_tp.user:
            return Response(
                {"error": "Can't match with same user"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Check if a match between the two timeplaces already exists
        queryset = Match.objects.filter(
            (Q(timeplace_1=own_tp) | Q(timeplace_1=other_tp)) &
            (Q(timeplace_2=own_tp) | Q(timeplace_2=other_tp))
        )

        if queryset:
            return Response(
                {"error": "Match already exists",
                "match_id": queryset[0].id},
                status=status.HTTP_403_FORBIDDEN
            )

        # Create a new match object and return the ID
        match_obj = Match.objects.create(
            timeplace_1=own_tp,
            timeplace_2=other_tp
        )
        return Response(
            {"match_id": match_obj.id},
            status=status.HTTP_201_CREATED
        )

    @extend_schema(responses=MatchModelListRetrieveSerializer(many=True))
    @action(detail=True, methods=["GET"], url_path="chats")
    def chats(self, request, *args, **kwargs):
        """View all active match-objects of a Timeplace
        """
        timeplace = self.get_object()
        queryset = (Match.objects
                    .exclude(deleted=True)
                    .filter(Q(timeplace_1=timeplace) |
                            Q(timeplace_2=timeplace))
                    .order_by("-created_at")
                    )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = MatchModelListRetrieveSerializer(page,
                                            context={'request': request},
                                            many=True)
            return self.get_paginated_response(serializer.data)

        serializer = MatchModelListRetrieveSerializer(queryset,
                                            context={'request': request},
                                            many=True)
        return Response(serializer.data)
