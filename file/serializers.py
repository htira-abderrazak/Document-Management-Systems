from directory.models import Directory
from rest_framework import serializers
from file.models import File
import os


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields =['id','name','directory','file','updated_at','created_at']

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
    def update(self, instance, validated_data):
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
        return super().update(instance, validated_data)
    file = serializers.FileField()

    def validate_file(self, value):
        # Access the file size
        file_size = value.size
        max_file_size = 10 * 1024 * 1024  # 10 MB
        if file_size > max_file_size:
            raise serializers.ValidationError("File size exceeds the allowed limit.")
        return value
    
def find_matching_folder(file_name, parent_folder_id):
    parent_folder = Directory.objects.get(id=parent_folder_id)

    # Generate all possible substrings of length 3 from the file name
    substrings = {file_name[i:i+n] for n in range(3, len(file_name)+1) for i in range(len(file_name) - n + 1)}
    print(substrings)
    # Search for folders with names containing any of the substrings
    matching_folders = Directory.objects.filter(parent=parent_folder, name__in=substrings)
    
    if matching_folders.exists():
        return matching_folders.first()
    else:
        return None