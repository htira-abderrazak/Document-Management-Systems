from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed
from .models import Directory
from .serializers import DirectorySerializer,DirectoryListSerializer
from rest_framework.views import APIView

# Create your views here.

class FolderViewSet(viewsets.ModelViewSet):
    queryset = Directory.objects.all()
    serializer_class = DirectoryListSerializer
    def list(self, request, *args, **kwargs):
        raise MethodNotAllowed("get")
    def retrieve(self, request, *args, **kwargs):
        raise MethodNotAllowed("get")
class GetFolder(APIView):

    def get(self,request,pk):
        try:
            folder = Directory.objects.get(id=pk)
        except Directory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        folder = DirectoryListSerializer(folder)
        return Response(folder.data)

