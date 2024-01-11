from django.db import models
import uuid
from directory.models import Directory
import os
from datetime import date

def get_upload_path(instance, filename):
    # Get today's date in the format 'YYYY-MM-DD'
    today_date = date.today().strftime('%Y-%m-%d')
    
    # Construct the upload path using the date
    upload_path = os.path.join('uploads', today_date)

    # Check if the folder exists, create it if not
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)

    # Return the final file path
    return os.path.join(upload_path, filename)


class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20,blank =True)
    directory = models.ForeignKey(Directory,on_delete=models.CASCADE)
    file = models.FileField(upload_to=get_upload_path, null=True, blank=True)
