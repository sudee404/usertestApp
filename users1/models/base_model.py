#models/base_model.py
from django.db import models
from django.utils import timezone
import uuid

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        abstract = True

class GenericBaseModel(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    #def save functionality
    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)



    #def delete functionality
    def delete(self, *args, **kwargs):
        self.is_active = False #soft
        super().save(*args, **kwargs)


    class Meta:
        abstract = True


