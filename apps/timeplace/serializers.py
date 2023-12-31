from datetime import datetime, timezone
import pytz
from rest_framework import serializers

from apps.user.serializers import UserModelSerializer
from apps.core.utils import get_nearest_city
from . import models


class InterestModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Interest
        fields = ["id","name"]


class ActivityModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Activity
        fields = ["id","name"]


class TimePlaceModelCreateSerializer(serializers.ModelSerializer):
    """Serializer to create a TimePlace model instance that takes interests 
    and activities as a list of integers and does not include the user.
    Automatically fills the city field with the nearest city to the given
    coordinates in a radius of 100 miles.
    """
    class Meta:
        model = models.TimePlace
        fields = [
            "id",
            "start",
            "end",
            "latitude",
            "longitude",
            "radius",
            "description",
            "interests",
            "activities"
        ]

    def validate(self, attrs):
        # We need to have all datetimes in the same timezone
        start_tz = attrs["start"].replace(tzinfo=pytz.UTC)
        end_tz = attrs["end"].replace(tzinfo=pytz.UTC)

        if start_tz < datetime.now(timezone.utc):
            raise serializers.ValidationError(
                "Start date has to be in the future.")
        if end_tz <= start_tz:
            raise serializers.ValidationError(
                "End date has to be after start date.")
        if attrs["latitude"] > 90 or attrs["latitude"] < -90:
            raise serializers.ValidationError(
                "Latitude has to be between +90° and -90°.")
        if attrs["longitude"] > 180 or attrs["longitude"] < -180:
            raise serializers.ValidationError(
                "Longitude has to be between +180° and -180°.")
        if attrs["radius"] > 50:
            raise serializers.ValidationError(
                "Radius can be 50km at most.")
        return attrs

    def create(self, validated_data):
        validated_data['city'] = get_nearest_city(
            validated_data['latitude'], validated_data['longitude'])
        return super(TimePlaceModelCreateSerializer, self).create(validated_data)

    def to_representation(self, instance):
        return (TimePlaceModelViewSerializer(context=self.context)
                .to_representation(instance))

class TimePlaceModelUpdateSerializer(serializers.ModelSerializer):
    """Serializer to update a TimePlace model instance that takes interests 
    and activities as a list of integers and does not include the user.
    """
    class Meta:
        model = models.TimePlace
        fields = [
            "id",
            "start",
            "end",
            "radius",
            "description",
            "interests",
            "activities"
        ]

    def validate(self, attrs):
        # We need to have all datetimes in the same timezone
        start_tz = attrs["start"].replace(tzinfo=pytz.UTC)
        end_tz = attrs["end"].replace(tzinfo=pytz.UTC)
        
        if start_tz < datetime.now(timezone.utc):
            raise serializers.ValidationError(
                "Start date has to be in the future.")
        if end_tz <= start_tz:
            raise serializers.ValidationError(
                "End date has to be after start date.")
        if attrs["radius"] > 50:
            raise serializers.ValidationError(
                "Radius can be 50km at most.")
        return attrs


class TimePlaceModelViewSerializer(serializers.ModelSerializer):
    """Serializer for the TimePlace model that includes detailed
    information about the user, interests and activities
    """
    user = UserModelSerializer()
    interests = InterestModelSerializer(many=True)
    activities = ActivityModelSerializer(many=True)

    class Meta:
        model = models.TimePlace
        fields = [
            "id",
            "user",
            "start",
            "end",
            "latitude",
            "longitude",
            "city",
            "radius",
            "description",
            "interests",
            "activities"
        ]


class TimePlaceModelAdminSerializer(serializers.ModelSerializer):
    """Serializer for the TimePlace model that includes detailed
    information about the user, interests and activities, including the
    deletion state
    """
    user = UserModelSerializer()
    interests = InterestModelSerializer(many=True)
    activities = ActivityModelSerializer(many=True)

    class Meta:
        model = models.TimePlace
        fields = [
            "id",
            "user",
            "start",
            "end",
            "latitude",
            "longitude",
            "city",
            "radius",
            "description",
            "interests",
            "activities",
            "deleted",
            "deleted_on"
        ]


class TimePlaceMatchSerializer(serializers.ModelSerializer):
    """Serializer to show the matches for a Timeplace
    """
    interests = InterestModelSerializer(many=True)
    activities = ActivityModelSerializer(many=True)
    username = serializers.CharField(source="user.userprofile.name")

    class Meta:
        model = models.TimePlace
        fields = [
            "id",
            "user",
            "username",
            "description",
            "interests",
            "activities",
        ]
