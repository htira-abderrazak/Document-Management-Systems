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