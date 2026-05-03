import uuid

from django.db import models


class BaseModel(models.Model):
    """
    Abstract base model that includes UUID as primary key,
    created_at, updated_at, and is_active fields.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
