# accounts/urls.py

from django.urls import path
from . import views # accounts 앱의 views.py를 임포트

app_name = 'accounts' # 앱 네임스페이스 설정 (필수)

urlpatterns = [
    # 기존 코드에서 잘려있던 부분
    # 예를 들어, /accounts/ 경로에 대한 profile_view가 있다면:
    path('', views.profile_view, name='profile'), # /accounts/ 로 접근 시 profile_view를 보여줌

    # 로그인 페이지 URL
    path('login/', views.login_view, name='login'),

    # 회원가입 페이지 URL (가장 중요)
    path('signup/', views.signup_view, name='signup'), # 'signup'이라는 name으로 views.signup_view 연결

    # 로그아웃 페이지 URL
    path('logout/', views.logout_view, name='logout'),

    # 추가했던 JSON 내보내기 URL (필요시)
    # path('export-json/', views.export_users_json, name='export_users_json'),
]