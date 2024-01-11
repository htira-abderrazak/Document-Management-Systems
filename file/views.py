from django.shortcuts import render
from rest_framework import viewsets
from .serializers import FileSerializer
from .models import File
# Create your views here.

class Fileviewset(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer