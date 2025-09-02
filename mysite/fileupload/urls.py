from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# FileViewSet을 위한 라우터 설정
router = DefaultRouter()
router.register(r'files', views.FileViewSet, basename='file')

urlpatterns = [
    # API 요청을 위한 라우터 URL을 포함
    path('', include(router.urls)),
    # 메인 페이지를 위한 URL
    path('main/', views.MainView.as_view(), name='main'),  
]
