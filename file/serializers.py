from rest_framework import serializers
from file.models import File


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields =['id','name','directory','file']

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
    