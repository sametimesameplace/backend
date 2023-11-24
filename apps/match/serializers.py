from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field, extend_schema_serializer
from drf_spectacular.utils import OpenApiTypes, OpenApiExample

from apps.timeplace import serializers as tp_serializers
from . import models


@extend_schema_serializer(
    examples = [
         OpenApiExample(
            'Example for a match object',
            summary='Example for a match object',
            value={
                    "id": 1,
                    "own_timeplace": {
                        "id": 13,
                        "user": 3,
                        "description": "Want to go to the Train Museum",
                        "interests": [
                        {
                            "id": 2,
                            "name": "Trains"
                        }
                        ],
                        "activities": [
                        {
                            "id": 1,
                            "name": "Visiting a Museum"
                        }
                        ]
                    },
                    "foreign_timeplace": {
                        "id": 2,
                        "user": 2,
                        "description": "Want to visit some kind of Museum",
                        "interests": [
                        {
                            "id": 2,
                            "name": "Trains"
                        }
                        ],
                        "activities": [
                        {
                            "id": 1,
                            "name": "Visiting a Museum"
                        }
                        ]
                    },
                    "foreign_email": None,
                    "foreign_phone": None,
                    "chat_accepted": False
                    },
        ),
    ]
)
class MatchModelListRetrieveSerializer(serializers.ModelSerializer):
    """Serializer for listing and retrieving matches"""

    own_timeplace = serializers.SerializerMethodField()
    foreign_timeplace = serializers.SerializerMethodField()
    foreign_email = serializers.SerializerMethodField()
    foreign_phone = serializers.SerializerMethodField()
    class Meta:
        model = models.Match
        fields = [
            "id",
            "own_timeplace",
            "foreign_timeplace",
            "foreign_email",
            "foreign_phone",
            "chat_accepted",
        ]

    @extend_schema_field(OpenApiTypes.OBJECT)    
    def get_own_timeplace(self, obj):
        """Returns the users own timeplace"""

        if obj.timeplace_1.user == self.context['request'].user:
            return tp_serializers.TimePlaceMatchSerializer(obj.timeplace_1).data
        return tp_serializers.TimePlaceMatchSerializer(obj.timeplace_2).data

    @extend_schema_field(OpenApiTypes.OBJECT)    
    def get_foreign_timeplace(self, obj):
        """Returns the timeplace of the matched user"""

        if obj.timeplace_1.user == self.context['request'].user:
            return tp_serializers.TimePlaceMatchSerializer(obj.timeplace_2).data
        return tp_serializers.TimePlaceMatchSerializer(obj.timeplace_1).data

    @extend_schema_field(OpenApiTypes.EMAIL)    
    def get_foreign_email(self, obj):
        """Returns the email of the matched user"""

        if obj.timeplace_1.user == self.context['request'].user:
            if obj.email_user_2:
                return obj.timeplace_2.user.userprofile.profile_email
            else:
                return None
        if obj.email_user_1:
            return obj.timeplace_1.user.userprofile.profile_email
        else:
            return None

    @extend_schema_field(OpenApiTypes.STR)    
    def get_foreign_phone(self, obj):
        """Returns the phone number of the matched user"""

        if obj.timeplace_1.user == self.context['request'].user:
            if obj.phone_user_2:
                return obj.timeplace_2.user.userprofile.phone
            else:
                return None
        if obj.phone_user_1:
            return obj.timeplace_1.user.userprofile.phone
        else:
            return None


class MatchChatModelSerializer(serializers.ModelSerializer):
    """Serializer for chat between matched users"""
    class Meta:
        model = models.MatchChat
        fields = [
            "id",
            "match_id",
            "user_id",
            "message",
        ]
