from django.db import transaction
from .tasks import transcribe_fileupload
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import FileUpload
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import FileSerializer
from django.views.generic import TemplateView

# 이전 FileUploadCreateView 클래스는 제거합니다.
# FileViewSet에서 모든 로직을 처리합니다.

class FileViewSet(viewsets.ModelViewSet):
    queryset = FileUpload.objects.all()
    serializer_class = FileSerializer

    # POST 요청을 처리할 create 메서드 오버라이딩
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # 파일이 성공적으로 저장된 후 Celery 작업 호출
        instance = serializer.instance
        task = transcribe_fileupload.delay(instance.pk)
        print(f"Task ID: {task.id}")

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class MainView(TemplateView):
    template_name = "fileupload/fileupload.html"
