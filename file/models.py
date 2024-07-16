from django.db import models
import uuid
from directory.models import Directory
import os
from datetime import date

import os
from datetime import date
from django.conf import settings

from user.models import User
def get_upload_path(instance, filename):
    today_date = date.today()

    year_folder = str(today_date.year)
    month_folder = str(today_date.month)
    day_folder = str(today_date.day)

    # Construct the relative upload path
    upload_path = os.path.join(year_folder, month_folder, day_folder)

    # Ensure the directory exists
    full_path = os.path.join(settings.MEDIA_ROOT, upload_path)
    if not os.path.exists(full_path):
        os.makedirs(full_path)

    return os.path.join(upload_path, filename)



class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50,blank =True)
    directory = models.ForeignKey(Directory,on_delete=models.CASCADE)
    file = models.FileField(upload_to=get_upload_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    favorite  = models.BooleanField(default=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True)

class Recent(models.Model):
    files = models.ForeignKey(File, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True, related_name='recentFiles')


