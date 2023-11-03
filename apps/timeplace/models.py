from django.db import models

from apps.core.models import CreatedModifiedDateTimeBase


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