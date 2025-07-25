# myusers/urls.py

from django.urls import path
from . import views # myusers 앱의 views.py를 임포트

app_name = 'myusers' # 앱 네임스페이스 설정 (필수)

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('export/', views.export_users_json, name='export_users_json'),
]