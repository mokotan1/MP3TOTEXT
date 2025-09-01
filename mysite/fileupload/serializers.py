from rest_framework import serializers
from .models import FileUpload
import whisper
from django.conf import settings
from fileupload.utils import get_whisper_model

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = ['id', 'file', 'description', 'uploaded_at', 'transcribed_txt']
        read_only_fields = ['uploaded_at', 'transcribed_txt']
    