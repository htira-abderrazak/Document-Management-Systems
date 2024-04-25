from celery import Celery
from file.models import File, TotalFileSize
from .models import Directory
from django.db.models import Q
from datetime import date
from datetime import timedelta
import os

app = Celery()

#define a 
@app.task
def periodic_delete():
    now = date.today()
    expiration_start = now - timedelta(hours=24)
    # Define the filter criteria using Q objects
    expired_query = Q(is_deleted = True, updated_at__lte=expiration_start)
    directories = Directory.objects.filter(expired_query)
    files = File.objects.filter(expired_query)
    directories.delete()
    total_size =TotalFileSize.objects.get(id=1)
    size = 0    
    for file in files:
        if os.path.isfile(file.file.path):
                os.remove(file.file.path)
        size -= file.file.size
    total_size.total_size= size/1024/1024
    total_size.save()
    files.delete()
