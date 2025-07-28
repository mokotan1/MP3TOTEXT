from rest_framework import serializers
from .models import fileupload
import whisper
from django.conf import settings
from fileupload.utils import get_whisper_model

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = fileupload
        fields = ['id', 'file', 'description', 'uploaded_at', 'transcirbed_txt']
        read_only_fields = ['uploaded_at', 'transcirbed_txt']
    