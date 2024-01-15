from celery import Celery
from file.models import File
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
    expired_query = Q(is_deleted = True, expired_date__lte=expiration_start)
    directories = Directory.objects.filter(expired_query)
    files = File.objects.filter(expired_query)
    directories.delete()
    for file in files:
        if os.path.isfile(file.file.path):
                os.remove(file.file.path)
    files.delete()
