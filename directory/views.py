import os

from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAuthenticated

from file.models import File,Recent as File_Recent
from file.serializers import FileSerializer

from .models import Directory, Recent

from .serializers import DirectorySerializer,DirectoryListSerializer,NavigationPaneSerializer,FoldeTreeSerializer

from datetime import date

# Create your views here.

#File Management View (update, delete , create)
class FolderViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset = Directory.objects.all()
    serializer_class = DirectorySerializer
    def list(self, request, *args, **kwargs):
        raise MethodNotAllowed("get")
    def retrieve(self, request, *args, **kwargs):
        raise MethodNotAllowed("get")
    # folder soft delete 
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.user :
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        self.Delete_children(instance)

        instance.is_deleted = True
        instance.expired_date = date.today()
        instance.save()
        return Response(status=204)
    
    def Delete_children(self,instance):
        if instance.children.exists():
            children = instance.children.all()
            for child in children:
                child.is_deleted = True
                child.expired_date = date.today()
                child.save()
                self.Delete_children(child)

#get folder content By ID View
class GetFolder(APIView):

    def get(self,request,pk):
        try:        
            folder = Directory.objects.get(id=pk,is_deleted= False)
        except Directory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if folder.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        recent_folders = Recent.objects.filter(user=request.user)

        if not recent_folders.filter(folders = folder).exists():
            if recent_folders.count() < 10 :
                Recent(folders =folder,user = request.user).save()
            else :
                #delte the oldest folder in recent and add the neww recent folder
                first = recent_folders.first()
                first.delete()
                Recent(folders =folder).save()
                
        folder = DirectoryListSerializer(folder)
        return Response(folder.data)

#Get All the root folders View
class GetRootFolders(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):

        folder = Directory.objects.filter(parent = None,is_deleted= False, user = request.user)

        folder = DirectorySerializer(folder,many=True)
        return Response(folder.data)
    
#get the Navigation Pnae View
class GetNavigationPane(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):

        
        folder = Directory.objects.filter(parent = None,is_deleted= False, user=request.user)

        folder = NavigationPaneSerializer(folder,many = True)
        return Response(folder.data)
    


#search files and folder by name
class SerchByname(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request,name):
        search_string = name
    
        folder = Directory.objects.filter(is_deleted= False,user=request.user,name__icontains=search_string)
        files = File.objects.filter(is_deleted= False,name__icontains=search_string,user=request.user)
        folder = DirectorySerializer(folder,many = True)
        files = FileSerializer(files,many = True)
        return Response([folder.data]+[files.data])
    
# get deleted files and folders
class GetTrash(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
    
        folder = Directory.objects.filter(is_deleted= True, user = request.user,parent__is_deleted = False)
        files = File.objects.filter(is_deleted= True , user = request.user)
        folder = DirectorySerializer(folder,many = True)
        files = FileSerializer(files,many = True)
        return Response([folder.data]+[files.data])
    
#get favorite files and folders
class GetFavorite(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
    
        folder = Directory.objects.filter(is_deleted= False,favorite = True, user = request.user)
        files = File.objects.filter(is_deleted= False,favorite = True, user = request.user)
        folder = DirectorySerializer(folder,many = True)
        files = FileSerializer(files,many = True)
        return Response([folder.data]+[files.data])
    
class GetRecent(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        recent_files = File_Recent.objects.filter(user = request.user)
        recent_folder = Recent.objects.filter(user = request.user)
        files = []
        folders= []
        for file in recent_files:
            files.append(FileSerializer(file.files).data)
        for folder in recent_folder:
            folders.append(DirectorySerializer(folder.folders).data)
        return Response([folders]+[files])


class CleanTrash(APIView):
    permission_classes=[IsAuthenticated]

    def delete(self,request):
        folder = Directory.objects.filter(is_deleted= True, user = request.user)
        files = File.objects.filter(is_deleted= True, user = request.user)
        user = request.user
        size = user.total_size
     
        paths =[] # store paths to delete them after deleting the 
        for file in files:
            if os.path.isfile(file.file.path):
                paths.append(file.file.path)

            size = size - file.file.size

        folder.delete()
        files.delete()
        for path in paths :
            if os.path.isfile(path):
                os.remove(path)
        if (size<1 and size>0):
            size = 1
        elif (size <0):
            size =0            
        user.total_size= size
        user.save()
        return Response(status=204)

class RestoreFolder(APIView):
    permission_classes=[IsAuthenticated]

    def put(self,request,id):
        try : 
            folder = Directory.objects.get(id = id,user = request.user)

        except Directory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if folder.is_deleted == True:
            folder.is_deleted = False
            folder.save()
        return Response(status=204)
    
class GetFoldersTree(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):

        
        folder = Directory.objects.filter(parent = None,is_deleted= False, user=request.user)

        folder = FoldeTreeSerializer(folder,many = True)
        return Response(folder.data)