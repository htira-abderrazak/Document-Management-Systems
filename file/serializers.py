from directory.models import Directory
from rest_framework import serializers
from file.models import File, TotalFileSize
import os


class FileSerializer(serializers.ModelSerializer):
    size = serializers.SerializerMethodField()
    class Meta:
        model = File
        fields =['id','name','directory','file','updated_at','created_at','size']

    file = serializers.FileField(required = True)
    def create(self, validated_data):
        if validated_data["directory"]:
            directories = File.objects.filter(directory = validated_data["directory"],name = validated_data["name"])
        else:
            directories = File.objects.filter(directory = None,name = validated_data["name"])
        if(directories.exists()):
            raise serializers.ValidationError(
                {"name": "this name already exists."}
            )
        matching_folder = find_matching_folder(validated_data["name"], validated_data["directory"].id)
        if matching_folder:
            validated_data["directory"]=matching_folder

        return super().create(validated_data)

    file = serializers.FileField()

    def validate_file(self, value):

        total_size =TotalFileSize.objects.get(id=1)

        # Access the file size
        file_size = value.size
        max_file_size = 10 * 1024 * 1024  # 10 MB
        if file_size > max_file_size and total_size.total_size< 100:
            raise serializers.ValidationError("File size exceeds the allowed limit.")
        total_size.total_size += (value.size /1024/1024)
        total_size.save()
        return value
    def get_size(self, obj):
        return obj.file.size / 1024
def find_matching_folder(file_name, parent_folder_id):
    parent_folder = Directory.objects.get(id=parent_folder_id)

    # Generate all possible substrings of length 3 from the file name
    substrings = {file_name[i:i+n] for n in range(3, len(file_name)+1) for i in range(len(file_name) - n + 1)}
    # Search for folders with names containing any of the substrings
    matching_folders = Directory.objects.filter(parent=parent_folder, name__in=substrings)
    
    if matching_folders.exists():
        return matching_folders.first()
    else:
        return None
    
#upadte name serializer
class FileSerializerUpdate(serializers.ModelSerializer):

    class Meta:
        model = File
        fields =['name','favorite']

    def update(self, instance, validated_data):
        # Check for 'name' in validated_data to avoid KeyError
        if 'name' in validated_data:
            # Validate unique name within the same directory
            if validated_data["name"] != instance.name:  # Check for change
                files = File.objects.filter(directory=instance.directory, name=validated_data["name"])
                if files.exists():
                    raise serializers.ValidationError({"name": "This name already exists."})
            instance.name = validated_data["name"]

        # Update favorite regardless of name change
        instance.favorite = validated_data.get('favorite', instance.favorite)  # Use get() for optional field
        instance.save()
        return instance