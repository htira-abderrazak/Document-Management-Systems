from rest_framework import serializers
from directory.models import Directory
from file.models import File
from file.serializers import FileSerializer
from rest_framework.exceptions import PermissionDenied

class DirectorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Directory
        fields = ['id','name','parent','created_at','updated_at','favorite']
    def create(self, validated_data):
        if validated_data["parent"]:
            directories = Directory.objects.filter(user = self.context['request'].user,parent = validated_data["parent"],name = validated_data["name"])
        else:
            directories = Directory.objects.filter(parent = None,name = validated_data["name"],user = self.context['request'].user)
        if(directories.exists()):
            raise serializers.ValidationError(
                {"name": "this name already exists."}
            )
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if self.context['request'].user != instance.user :
            raise PermissionDenied('no permission')
        # Check for 'name' in validated_data to avoid KeyError
        if 'name' in validated_data:
            # Validate unique name within the same directory
            if validated_data["name"] != instance.name:  # Check for change
                directories = Directory.objects.filter(parent = instance.parent,name = validated_data["name"],user = self.context['request'].user)
                if directories.exists():
                    raise serializers.ValidationError({"name": "This name already exists."})
            instance.name = validated_data["name"]
            
        # Update favorite regardless of name change
        instance.favorite = validated_data.get('favorite', instance.favorite)  # Use get() for optional field
        instance.save()
        return instance
    

class DirectoryListSerializer(serializers.ModelSerializer):
    adress = serializers.SerializerMethodField()
    folders = serializers.SerializerMethodField()
    files = serializers.SerializerMethodField()
    class Meta:
        model = Directory
        fields = ['adress','folders','files','id','updated_at','created_at']
    def get_adress(self, obj):
        adress = []
        current_folder = obj
        while current_folder:
            adress.insert(0,[current_folder.name,current_folder.id])
            current_folder = current_folder.parent
        return adress
    def get_folders(self, obj):
        folders = Directory.objects.filter(parent = obj,is_deleted = False)
        data = DirectorySerializer(folders, many=True).data
        return data
    def get_files(self,obj):
        files = File.objects.filter(directory = obj,is_deleted = False)
        data =  FileSerializer(files,many = True).data
        return data


class NavigationPaneSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    class Meta:
        model = Directory
        fields = ['id','name','content']
    def get_content(self, obj):
        folders = Directory.objects.filter(parent = obj,is_deleted=False)
        if folders.exists():
            folders = NavigationPaneSerializer(folders,many = True).data
        files = File.objects.filter(directory = obj,is_deleted = False)
        files =  FileSerializer(files,many = True).data
        return {
            'folders': folders,
            'files': files,
        }
    
class FoldeTreeSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    class Meta:
        model = Directory
        fields = ['id','name','content']
    def get_content(self, obj):
        folders = Directory.objects.filter(parent = obj,is_deleted=False)
        if folders.exists():
            folders = FoldeTreeSerializer(folders,many = True).data

        return folders
        
    