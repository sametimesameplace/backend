from rest_framework import serializers

from . import models


class InterestModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Interest
        fields = "__all__"


class ActivityModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Activity
        fields = "__all__"
        