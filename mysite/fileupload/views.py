from django.shortcuts import redirect, render
from .forms import fileUploadForm
from .models import fileupload
from django.conf import settings
from rest_framework import viewsets
from .serializers import FileSerializer



class FileViewSet(viewsets.ModelViewSet):
    queryset = fileupload.objects.all()
    serializer_class = FileSerializer


def upload_file(request):
    # 업로드된 파일을 미리 확인
    upload_files = fileupload.objects.all()

    return render(request, 'fileupload/fileupload.html', 
    {
        'upload_files': upload_files,
    })

    