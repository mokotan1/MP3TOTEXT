from django.shortcuts import redirect, render
from .forms import fileUploadForm
from .models import fileupload
from django.conf import settings
from rest_framework import viewsets
from .serializers import FileSerializer
from .utils import get_whisper_model



class FileViewSet(viewsets.ModelViewSet):
    serializer_class = FileSerializer

    def perform_create(self, serializer):

        serializer.save()
        file_path = serializer.instance.file.path

        whisper_model = get_whisper_model()

        return_txt = whisper_model.transcribe(file_path, language = 'ko')

        serializer.instance.transcribed_txt = return_txt['text']

        serializer.instance.save()

    



def upload_file(request):
    # 업로드된 파일을 미리 확인
    upload_files = fileupload.objects.all()

    return render(request, 'fileupload/fileupload.html', 
    {
        'upload_files': upload_files,
    })

    