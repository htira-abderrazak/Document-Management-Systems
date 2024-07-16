from django.db import models

import uuid

from user.models import User

# Create your models here.
class Directory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50,blank =True)
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_deleted = models.BooleanField(default=False)
    favorite  = models.BooleanField(default=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True)

#model for store the recent files and folders
class Recent(models.Model):
    folders = models.ForeignKey(Directory, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True)
