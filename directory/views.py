from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import MethodNotAllowed

from file.models import File
from file.serializers import FileSerializer

from .models import Directory

from .serializers import DirectorySerializer,DirectoryListSerializer,NavigationPaneSerializer

from datetime import date

# Create your views here.

#File Management View (update, delete , create)
class FolderViewSet(viewsets.ModelViewSet):
    queryset = Directory.objects.all()
    serializer_class = DirectorySerializer
    def list(self, request, *args, **kwargs):
        raise MethodNotAllowed("get")
    def retrieve(self, request, *args, **kwargs):
        raise MethodNotAllowed("get")
    # folder soft delete 
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.expired_date = date.today()
        instance.save()
        return Response(status=204)
    
#get folder content By ID View
class GetFolder(APIView):

    def get(self,request,pk):
        try:
            folder = Directory.objects.get(id=pk,is_deleted= False)
        except Directory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        folder = DirectoryListSerializer(folder)
        return Response(folder.data)

#Get All the root folders View
class GetRootFolders(APIView):

    def get(self,request):


        folder = Directory.objects.filter(parent = None,is_deleted= False)


        folder = DirectorySerializer(folder,many=True)
        return Response(folder.data)
    
#get the Navigation Pnae View
class GetNavigationPane(APIView):
    def get(self,request):

        
        folder = Directory.objects.filter(parent = None,is_deleted= False)

        folder = NavigationPaneSerializer(folder,many = True)
        return Response(folder.data)
    


#search files and folder by name
class SerchByname(APIView):
    def get(self,request,name):
        search_string = name
    
        folder = Directory.objects.filter(is_deleted= False,name__icontains=search_string)
        files = File.objects.filter(is_deleted= False,name__icontains=search_string)
        folder = DirectorySerializer(folder,many = True)
        files = FileSerializer(files,many = True)
        return Response([folder.data]+[files.data])
    
# get deleted files and folders
class GetTrash(APIView):
    def get(self,request):
    
        folder = Directory.objects.filter(is_deleted= True)
        files = File.objects.filter(is_deleted= True)
        folder = DirectorySerializer(folder,many = True)
        files = FileSerializer(files,many = True)
        return Response([folder.data]+[files.data])
    
#get favorite files and folders
class GetFavorite(APIView):
    def get(self,request):
    
        folder = Directory.objects.filter(is_deleted= False,favorite = True)
        files = File.objects.filter(is_deleted= False,favorite = True)
        folder = DirectorySerializer(folder,many = True)
        files = FileSerializer(files,many = True)
        return Response([folder.data]+[files.data])