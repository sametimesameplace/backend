from django.db import models

class CreatedModifiedDateTimeBase(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDelete(models.Model):
    """Abstract model to include fields for softdelete functionality.
    """
    deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        abstract = True