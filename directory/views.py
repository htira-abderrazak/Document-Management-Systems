from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import MethodNotAllowed

from .models import Directory

from .serializers import DirectorySerializer,DirectoryListSerializer,NavigationPaneSerializer
# Create your views here.

#File Management View (update, delete , create)
class FolderViewSet(viewsets.ModelViewSet):
    queryset = Directory.objects.all()
    serializer_class = DirectorySerializer
    def list(self, request, *args, **kwargs):
        raise MethodNotAllowed("get")
    def retrieve(self, request, *args, **kwargs):
        raise MethodNotAllowed("get")
    
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