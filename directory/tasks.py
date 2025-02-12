from celery import Celery
from file.models import File
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
    paths =[] # store paths to delete them after deleting the 
    for file in files:
        if os.path.isfile(file.file.path):
            paths.append(file.file.path)
        user = file.user
        totalSize = user.total_size - file.file.size
        user.total_size = totalSize
        file.user.save()
        
    folders.delete()
    files.delete()
    for path in paths :
        if os.path.isfile(path):
            os.remove(path)
