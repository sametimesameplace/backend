from django.db import models

from apps.user.models import User
from apps.timeplace.models import TimePlace
from apps.core.models import CreatedModifiedDateTimeBase, SoftDelete


class Match(CreatedModifiedDateTimeBase, SoftDelete):
    """Model to store the matches between users"""

    timeplace_1 = models.ForeignKey(
        "timeplace.TimePlace", on_delete=models.CASCADE, related_name="timeplace_1"
    )
    timeplace_2 = models.ForeignKey(
        "timeplace.TimePlace", on_delete=models.CASCADE, related_name="timeplace_2"
    )
    email_user_1 = models.BooleanField(default=False)
    email_user_2 = models.BooleanField(default=False)
    phone_user_1 = models.BooleanField(default=False)
    phone_user_2 = models.BooleanField(default=False)
    chat_accepted = models.BooleanField(default=False)


class MatchChat(CreatedModifiedDateTimeBase):
    """Model to store the chat between users"""

    match_id = models.ForeignKey("match.Match", on_delete=models.CASCADE)
    user_id = models.ForeignKey("user.User", on_delete=models.CASCADE)
    message = models.TextField(max_length=500)
