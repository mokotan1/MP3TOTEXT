from rest_framework import serializers
from .models import FileUpload
from fileupload.utils import get_whisper_model

class FileSerializer(serializers.ModelSerializer):
    """
    FileUpload 모델을 위한 시리얼라이저입니다.
    """
    class Meta:
        model = FileUpload
        fields = ['id', 'file', 'description', 'uploaded_at', 'transcribed_txt']
        read_only_fields = ['uploaded_at', 'transcribed_txt']
