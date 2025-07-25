# myusers/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.http import JsonResponse, HttpResponse
import json
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import get_user_model
User = get_user_model()

from .forms import CustomUserCreationForm # 수정된 폼 임포트

@login_required
def profile_view(request):
    return HttpResponse(f"<h1>{request.user.username}님의 프로필 페이지입니다.</h1><p>로그인에 성공하셨습니다!</p>")


@csrf_exempt
def signup_view(request):
    if request.method == 'GET':
        form = CustomUserCreationForm() # GET 요청 시 폼 인스턴스 생성
        return render(request, 'myusers/signup.html', {'form': form})
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(f"Received data from client: {data}") # 디버깅 출력

            # CustomUserCreationForm에 JSON 데이터를 직접 전달합니다.
            # 이제 폼은 'username', 'password', 'password2' 필드를 기대합니다.
            form = CustomUserCreationForm(data)
            print(f"Form data passed to CustomUserCreationForm: {form.data}") # 디버깅 출력

            if form.is_valid():
                user = form.save() # 폼의 save 메서드를 호출하여 사용자 생성
                login(request, user)
                return JsonResponse({"message": "회원가입이 성공적으로 완료되었습니다.", "redirect_url": "/"}, status=201)
            else:
                errors_dict = form.errors.as_data()
                processed_errors = {}
                for field, errors in errors_dict.items():
                    processed_errors[field] = [str(error.message) for error in errors]

                print(f"Form errors: {processed_errors}") # 디버깅 출력

                return JsonResponse({
                    "message": "회원가입 정보에 오류가 있습니다.",
                    "errors": processed_errors
                }, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"message": "잘못된 요청 형식입니다. JSON 데이터를 보내주세요."}, status=400)
        except Exception as e:
            print(f"Server Error during signup: {e}")
            return JsonResponse({"message": f"서버 오류가 발생했습니다: {str(e)}"}, status=500)


def login_view(request):
    return HttpResponse("<h1>로그인 페이지입니다.</h1><p>로그인 기능이 곧 구현될 예정입니다.</p>")

def logout_view(request):
    logout(request)
    return redirect('/')

@staff_member_required
def export_users_json(request):
    users_data = []
    for user in User.objects.all().order_by('username'):
        users_data.append({
            'username': user.username,
            'password_hash': user.password
        })
    return JsonResponse(users_data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 4})
