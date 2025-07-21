from rest_framework import serializers
from .models import fileupload

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = fileupload
        fields = ['id', 'file', 'description', 'uploaded_at']