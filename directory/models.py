from django.db import models
import uuid

# Create your models here.
class Directory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20,blank =True)
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True, blank=True)