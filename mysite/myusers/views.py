# myusers/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse, HttpResponse
import json
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import get_user_model
User = get_user_model()

from .forms import CustomUserCreationForm

@login_required
def profile_view(request):
    return HttpResponse(f"<h1>{request.user.username}님의 프로필 페이지입니다.</h1><p>로그인에 성공하셨습니다!</p>")


@csrf_exempt
def signup_view(request):
    if request.method == 'GET':
        form = CustomUserCreationForm()
        return render(request, 'myusers/signup.html', {'form': form})
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(f"Received data from client: {data}")

            form = CustomUserCreationForm(data)
            print(f"Form data passed to CustomUserCreationForm: {form.data}")

            if form.is_valid():
                user = form.save()
                # 회원가입 후 자동으로 로그인 시키는 대신, 로그인 페이지로 리디렉션합니다.
                # login(request, user) # 이 줄은 필요에 따라 주석 처리하거나 제거할 수 있습니다.

                # 성공 시 로그인 페이지로 리디렉션하도록 URL을 변경합니다.
                return JsonResponse({"message": "회원가입이 성공적으로 완료되었습니다. 로그인 페이지로 이동합니다.", "redirect_url": "/accounts/login/"}, status=201)
            else:
                errors_dict = form.errors.as_data()
                processed_errors = {}
                for field, errors in errors_dict.items():
                    processed_errors[field] = [str(error.message) for error in errors]

                print(f"Form errors: {processed_errors}")

                return JsonResponse({
                    "message": "회원가입 정보에 오류가 있습니다.",
                    "errors": processed_errors
                }, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"message": "잘못된 요청 형식입니다. JSON 데이터를 보내주세요."}, status=400)
        except Exception as e:
            print(f"Server Error during signup: {e}")
            return JsonResponse({"message": f"서버 오류가 발생했습니다: {str(e)}"}, status=500)


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                # 로그인 성공 시 메인 페이지로 리디렉션하도록 URL을 변경합니다.
                return JsonResponse({"message": "로그인 성공!", "redirect_url": "/main/"}, status=200)
            else:
                return JsonResponse({"message": "로그인 실패: 아이디 또는 비밀번호가 올바르지 않습니다."}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"message": "잘못된 요청 형식입니다. JSON 데이터를 보내주세요."}, status=400)
        except Exception as e:
            print(f"Server Error during login: {e}")
            return JsonResponse({"message": f"서버 오류가 발생했습니다: {str(e)}"}, status=500)
    else: # GET 요청 시 로그인 폼 렌더링
        form = AuthenticationForm()
        return render(request, 'myusers/login.html', {'form': form})


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
