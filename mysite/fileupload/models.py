from django.db import models

# 모델 정의 시작

class fileupload(models.Model):
    #  upload_to는 파일을 media/uploads/에 저장
    file = models.FileField(upload_to='uploads/')
    description = models.CharField(max_length = 255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.file.name
# 모델 정의 끝