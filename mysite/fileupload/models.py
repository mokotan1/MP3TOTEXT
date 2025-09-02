from django.db import models

class FileUpload(models.Model):
    """
    업로드된 파일 정보를 저장하는 모델입니다.
    """
    file = models.FileField(upload_to='uploads/')
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    transcribed_txt = models.TextField(blank=True)
    
    def __str__(self):
        return self.file.name
