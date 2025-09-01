from django.db import transaction  # 최상단에 추가
from .tasks import transcribe_fileupload
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import FileUpload
from rest_framework import viewsets
import fileupload
from .serializers import FileSerializer
from django.views.generic import TemplateView





class FileUploadCreateView(CreateView):
    model = FileUpload
    fields = ["file", "description"]
    template_name = "fileupload/fileupload.html"
    success_url = reverse_lazy("fileupload_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        print(f"DEBUG: {self.object.pk}")
        # DB commit 이후에 task 실행
        transcribe_fileupload.delay(self.object.pk)
        return response

class FileViewSet(viewsets.ModelViewSet):
    queryset = FileUpload.objects.all()
    serializer_class = FileSerializer



class MainView(TemplateView):
    template_name = "fileupload/fileupload.html"  # 실제 HTML 파일 경로



