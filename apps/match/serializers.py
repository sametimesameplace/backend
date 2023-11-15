from rest_framework import serializers

from . import models


class MatchModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Match
        fields = [
            "id",
            "timeplace_1",
            "timeplace_2",
            "email_user_1",
            "email_user_2",
            "phone_user_1",
            "phone_user_2",
            "chat_accepted",
        ]


class MatchChatModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MatchChat
        fields = [
            "id",
            "match_id",
            "user_id",
            "message",
        ]
