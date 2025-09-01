from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('fileupload.urls')),   # API 및 HTML 업로드 폼 포함
    path('users/', include('myusers.urls', namespace='myusers')),  # myusers 앱 추가
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)