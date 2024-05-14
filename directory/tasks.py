from celery import Celery
from file.models import File, TotalFileSize
from .models import Directory
from django.db.models import Q
from datetime import timedelta
import os
from django.utils import timezone
app = Celery()

#define a 
@app.task
def periodic_delete():
    now = timezone.now()

    # Calculate the time one minute ago with timezone awareness
    expiration_start = now - timedelta(hours=24)

    folders = Directory.objects.filter(is_deleted = True, updated_at__lte=expiration_start)
    files = File.objects.filter(is_deleted = True, updated_at__lte=expiration_start)
    total_size =TotalFileSize.objects.get(id=1)
    size = total_size.total_size  
    paths =[] # store paths to delete them after deleting the 
    for file in files:
        if os.path.isfile(file.file.path):
            paths.append(file.file.path)
        size = size - (file.file.size /1024 /1024)
    folders.delete()
    files.delete()
    for path in paths :
        if os.path.isfile(path):
            os.remove(path)
    if (size<0):
        size = 0
    total_size.total_size= int(size)
    total_size.save()
