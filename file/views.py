from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import FileSerializer
from .models import File
# Create your views here.

class Fileviewset(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def get_queryset(self):

        return self.queryset.filter(is_deleted=False)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=204)