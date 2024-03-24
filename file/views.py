from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.views import APIView

from .serializers import FileSerializer, FileSerializerUpdate
from .models import File
from datetime import date
# Create your views here.

class Fileviewset(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    def get_serializer_class(self):
        if self.action == 'update':
            return FileSerializerUpdate

        return super().get_serializer_class()
    def get_queryset(self):

        return self.queryset.filter(is_deleted=False)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.expired_date = date.today()
        instance.save()
        return Response(status=204)
    def retrieve(self, request, *args, **kwargs):
        raise MethodNotAllowed("get")
    def list(self, request, *args, **kwargs):
        raise MethodNotAllowed("get")

        
    

