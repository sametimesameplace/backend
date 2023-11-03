from datetime import datetime
from rest_framework import serializers

from apps.user.serializers import UserModelSerializer
from . import models


class InterestModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Interest
        fields = "__all__"


class ActivityModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Activity
        fields = "__all__"


class TimePlaceModelSerializer(serializers.ModelSerializer):
    user_id = UserModelSerializer()
    interests = InterestModelSerializer(many=True)
    activities = ActivityModelSerializer(many=True)

    class Meta:
        model = models.TimePlace
        fields = [
            "id",
            "user_id",
            "start",
            "end",
            "latitude",
            "longitude",
            "description",
            "interests",
            "activities"
        ]

    def validate(self, data):
        if data['start'] < datetime.now():
            raise serializers.ValidationError(
                "Start date has to be in the future.")
        if data["end"] <= data["start"]:
            raise serializers.ValidationError(
                "End date has to be after start date.")
        if data["latitude"] > 90 or data["latitude"] < -90:
            raise serializers.ValidationError(
                "Latitude has to be between +90° and -90°")
        if data["longitude"] > 180 or data["longitude"] < -180:
            raise serializers.ValidationError(
                "Longitude has to be between +180° and -180°")
        return data
