from django.db import models

from apps.core.models import CreatedModifiedDateTimeBase, SoftDelete
from apps.user.models import User


class Interest(CreatedModifiedDateTimeBase):
    """Model to store the various interests that can be used for filtering
    """
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name


class Activity(CreatedModifiedDateTimeBase):
    """Model to store the various Activities that can be used for filtering
    """
    name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        verbose_name_plural = "Activities"
    
    def __str__(self):
        return self.name


class TimePlace(CreatedModifiedDateTimeBase, SoftDelete):
    """Model to store the Timeplaces that a user creates
    """
    user = models.ForeignKey(
        "user.User", on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    radius = models.PositiveSmallIntegerField()
    description = models.CharField(max_length=500)
    interests = models.ManyToManyField("timeplace.Interest")
    activities = models.ManyToManyField("timeplace.Activity")
