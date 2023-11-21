from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from apps.timeplace import serializers as tp_serializers
from . import models

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
        
    def get_own_timeplace(self, obj):
        """Returns the users own timeplace"""
        
        if obj.timeplace_1.user == self.context['request'].user:
            return tp_serializers.TimePlaceModelViewSerializer(obj.timeplace_1).data
        return tp_serializers.TimePlaceModelViewSerializer(obj.timeplace_2).data
    
    def get_foreign_timeplace(self, obj):
        """Returns the timeplace of the matched user"""
        
        if obj.timeplace_1.user == self.context['request'].user:
            return tp_serializers.TimePlaceModelViewSerializer(obj.timeplace_2).data
        return tp_serializers.TimePlaceModelViewSerializer(obj.timeplace_1).data
    
    def get_foreign_email(self, obj):
        """Returns the email of the matched user"""
        
        if obj.timeplace_1.user == self.context['request'].user:
            if obj.email_user_2:
                return obj.timeplace_2.user.userprofile.profile_email
            else:
                return "Hidden"
        if obj.email_user_1:
            return obj.timeplace_1.user.userprofile.profile_email
        else:
            return "Hidden"
    
    def get_foreign_phone(self, obj):
        """Returns the phone number of the matched user"""
        
        if obj.timeplace_1.user == self.context['request'].user:
            if obj.phone_user_2:
                return obj.timeplace_2.user.userprofile.phone
            else:
                return "Hidden"
        if obj.phone_user_1:
            return obj.timeplace_1.user.userprofile.phone
        else:
            return "Hidden"
       
            
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
