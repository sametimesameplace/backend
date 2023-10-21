from django.db import models

class CreatedModifiedDateTimeBase(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    class Meta:         # Turns the class in an abstract base class so no tables are created
        abstract = True