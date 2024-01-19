from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed
from .models import Directory
from .serializers import DirectorySerializer,DirectoryListSerializer,NavigationPaneSerializer
from rest_framework.views import APIView
from django.http import JsonResponse
# Create your views here.

class FolderViewSet(viewsets.ModelViewSet):
    queryset = Directory.objects.all()
    serializer_class = DirectorySerializer
    def list(self, request, *args, **kwargs):
        raise MethodNotAllowed("get")
    def retrieve(self, request, *args, **kwargs):
        raise MethodNotAllowed("get")
class GetFolder(APIView):

    def get(self,request,pk):
        try:
            folder = Directory.objects.get(id=pk,is_deleted= False)
        except Directory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        folder = DirectoryListSerializer(folder)
        return Response(folder.data)

class GetRootFolders(APIView):

    def get(self,request):


        folder = Directory.objects.filter(parent = None,is_deleted= False)


        folder = DirectorySerializer(folder,many=True)
        return Response(folder.data)
    
class GetNavigationPane(APIView):
    def get(self,request):


        folder = Directory.objects.filter(parent = None,is_deleted= False)

        folder = NavigationPaneSerializer(folder,many = True)
        return Response(folder.data)