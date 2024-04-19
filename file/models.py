from django.db import models
import uuid
from directory.models import Directory
import os
from datetime import date

def get_upload_path(instance, filename):
    today_date = date.today()

    year_folder = str(today_date.year)
    month_folder = str(today_date.month)
    day_folder = str(today_date.day)

    upload_path = os.path.join('uploads', year_folder, month_folder, day_folder)

    # Check if the year folder exists, create it if not
    if not os.path.exists(os.path.join('uploads', year_folder)):
        os.makedirs(os.path.join('uploads', year_folder))

    # Check if the month folder exists, create it if not
    if not os.path.exists(os.path.join('uploads', year_folder, month_folder)):
        os.makedirs(os.path.join('uploads', year_folder, month_folder))

    # Check if the day folder exists, create it if not
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)

    return os.path.join(upload_path, filename)


class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50,blank =True)
    directory = models.ForeignKey(Directory,on_delete=models.CASCADE)
    file = models.FileField(upload_to=get_upload_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    expired_date = models.DateField(null=True, blank=True)
    favorite  = models.BooleanField(default=False)

class Recent(models.Model):
    files = models.ForeignKey(File, on_delete=models.CASCADE)