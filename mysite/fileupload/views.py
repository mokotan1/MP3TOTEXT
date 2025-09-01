from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import FileUpload
from rest_framework import viewsets
import fileupload
from .tasks import transcribe_fileupload


class FileUploadCreateView(CreateView):
    model = FileUpload
    fields = ["file", "description"]
    success_url = reverse_lazy("fileupload_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        transcribe_fileupload.delay(self.object.pk)
        return response
    
from .serializers import FileSerializer

class FileViewSet(viewsets.ModelViewSet):
    queryset = FileUpload.objects.all()
    serializer_class = FileSerializer



