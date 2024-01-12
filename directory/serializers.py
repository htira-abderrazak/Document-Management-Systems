from rest_framework import serializers
from directory.models import Directory

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