from rest_framework import serializers
from directory.models import Directory

class DirectorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Directory
        fields = '__all__'
