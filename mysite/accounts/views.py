# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.http import JsonResponse, HttpResponse
import json
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User

# 이 main_view는 mysite/urls.py에서 메인 페이지('/')로 연결되어 있으므로,
# accounts 앱의 views.py에는 더 이상 메인 페이지 역할을 할 필요가 없습니다.
# 하지만 필요하다면 다른 용도로 유지할 수 있습니다.
# def main_view(request):
#     if request.user.is_authenticated:
#         message = f"{request.user.username}님, 환영합니다!"
#     else:
#         message = "환영합니다! 로그인하거나 회원가입을 해주세요."
#     return HttpResponse(f"<h1>{message}</h1><p>여기는 메인 페이지입니다. 콘텐츠가 곧 추가될 예정입니다.</p>")

@login_required # 이 뷰는 로그인한 사용자만 접근 가능
def profile_view(request):
    """
    사용자 프로필 페이지를 렌더링합니다.
    accounts 앱의 루트 경로 ('/accounts/')로 접근 시 보여질 페이지입니다.
    """
    return HttpResponse(f"<h1>{request.user.username}님의 프로필 페이지입니다.</h1><p>로그인에 성공하셨습니다!</p>")


def signup_view(request):
    if request.method == 'GET':
        form = CustomUserCreationForm()
        return render(request, 'accounts/signup.html', {'form': form})
    # ... (기존 POST 요청 처리 로직은 그대로 유지)
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = CustomUserCreationForm(data)

            if form.is_valid():
                user = form.save()
                login(request, user)

                return JsonResponse({"message": "회원가입이 성공적으로 완료되었습니다.", "redirect_url": "/"}, status=201)
            else:
                errors_dict = form.errors.as_data()
                processed_errors = {}
                for field, errors in errors_dict.items():
                    processed_errors[field] = [str(error.message) for error in errors]

                return JsonResponse({
                    "message": "회원가입 정보에 오류가 있습니다.",
                    "errors": processed_errors
                }, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"message": "잘못된 요청 형식입니다. JSON 데이터를 보내주세요."}, status=400)
        except Exception as e:
            return JsonResponse({"message": f"서버 오류가 발생했습니다: {str(e)}"}, status=500)


def login_view(request):
    # 실제 로그인 폼 렌더링 및 처리 로직 필요
    return HttpResponse("<h1>로그인 페이지입니다.</h1><p>로그인 기능이 곧 구현될 예정입니다.</p>")

def logout_view(request):
    logout(request)
    return redirect('/')

# --- JSON 파일 내보내기 기능 추가 ---
@staff_member_required # 관리자(is_staff=True)만 이 뷰에 접근 가능
def export_users_json(request):
    users_data = []
    # 데이터베이스에서 모든 User 객체를 가져와 username 순으로 정렬
    for user in User.objects.all().order_by('username'):
        users_data.append({
            'username': user.username,
            'password_hash': user.password # 비밀번호는 해싱된 형태로 저장되어 있습니다.
        })

    # JsonResponse를 사용하여 JSON 응답을 보냅니다.
    # safe=False는 딕셔너리가 아닌 리스트도 최상위 레벨로 허용합니다.
    # ensure_ascii=False는 한글 등의 유니코드 문자가 깨지지 않도록 합니다.
    # indent=4는 JSON 출력의 가독성을 높입니다.
    return JsonResponse(users_data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 4})