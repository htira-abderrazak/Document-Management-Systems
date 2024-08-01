from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

import uuid
# Create your models here.

    
class User(AbstractUser):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    total_size = models.PositiveIntegerField(default=0)
    max_size = models.PositiveIntegerField(default=100)