from django.http import JsonResponse
from django.shortcuts import render

from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .serializers import FileSerializer, FileSerializerUpdate
from .models import File
from datetime import date
# Create your views here.

#file management View (create, update, Delete)
class Fileviewset(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    def get_serializer_class(self):
        if self.action == 'update':
            return FileSerializerUpdate

        return super().get_serializer_class()
    def get_queryset(self):

        return self.queryset.filter(is_deleted=False)

    #soft delete file
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.user != instance.user :
            return Response(status=status.HTTP_403_FORBIDDEN)        
        instance.is_deleted = True
        instance.expired_date = date.today()
        instance.save()
        return Response(status=204)
    def retrieve(self, request, *args, **kwargs):
        raise MethodNotAllowed("get")
    def list(self, request, *args, **kwargs):
        raise MethodNotAllowed("get")

        
    
class GetTotalSize(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        

        return JsonResponse({"total-size":request.user.total_size,"max-size": request.user.max_size})


class RestoreFile(APIView):
    permission_classes=[IsAuthenticated]

    def put(self,request,id):
        try : 
            file = File.objects.get(id = id,user=  request.user)

        except File.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if file.is_deleted == True :
            file.is_deleted = False
            file.save()
        return Response(status=204)