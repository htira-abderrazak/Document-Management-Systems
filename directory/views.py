from django.shortcuts import render
from rest_framework import viewsets
from .models import Directory
from .serializers import DirectorySerializer

# Create your views here.

class FolderViewSet(viewsets.ModelViewSet):
    queryset = Directory.objects.all()
    serializer_class = DirectorySerializer