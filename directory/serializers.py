from rest_framework import serializers
from directory.models import Directory
from file.models import File
from file.serializers import FileSerializer
class DirectorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Directory
        fields = ['id','name','parent','created_at','updated_at']
    def create(self, validated_data):
        if validated_data["parent"]:
            directories = Directory.objects.filter(parent = validated_data["parent"],name = validated_data["name"])
        else:
            directories = Directory.objects.filter(parent = None,name = validated_data["name"])
        if(directories.exists()):
            raise serializers.ValidationError(
                {"name": "this name already exists."}
            )
        return super().create(validated_data)
    

class DirectoryListSerializer(serializers.ModelSerializer):
    root = serializers.SerializerMethodField()
    folders = serializers.SerializerMethodField()
    files = serializers.SerializerMethodField()
    class Meta:
        model = Directory
        fields = ['root','folders','files','id']
    def get_root(self, obj):
        root = []
        current_folder = obj
        while current_folder:
            root.append(f"{current_folder.name}")
            current_folder = current_folder.parent

        # Join the list to create the root chain string
        return " / ".join(root)
    def get_folders(self, obj):
        folders = Directory.objects.filter(parent = obj,is_deleted = False)
        data = DirectorySerializer(folders, many=True).data
        return data
    def get_files(self,obj):
        files = File.objects.filter(directory = obj,is_deleted = False)
        data =  FileSerializer(files,many = True).data
        return data
