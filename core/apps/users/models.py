import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import ImageField


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    avatar = ImageField(upload_to='users/', max_length=255, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.email}"
    
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
