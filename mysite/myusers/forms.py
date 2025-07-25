from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError # ValidationError 임포트

User = get_user_model()

class CustomUserCreationForm(forms.Form): # forms.Form을 상속받습니다.
    username = forms.CharField(label="아이디", max_length=150,
                               widget=forms.TextInput(attrs={'placeholder': '사용할 닉네임을 입력하세요'}))
    password = forms.CharField(label="비밀번호", widget=forms.PasswordInput(attrs={'placeholder': '비밀번호를 입력하세요'}))
    password2 = forms.CharField(label="비밀번호 확인", widget=forms.PasswordInput(attrs={'placeholder': '비밀번호를 다시 입력하세요'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if not username.isalnum(): # 영문자와 숫자만 허용
            raise ValidationError("아이디는 영문자와 숫자만 사용할 수 있습니다.")
        if User.objects.filter(username=username).exists():
            raise ValidationError("이미 존재하는 아이디입니다.")
        return username

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password and password2 and password != password2:
            raise ValidationError("비밀번호가 일치하지 않습니다.")

        # 비밀번호 정책 (최소 8자리, 영문/숫자/특수기호 포함)
        if password and len(password) < 8:
            raise ValidationError("비밀번호는 최소 8자리 이상이어야 합니다.")
        
        has_letter = any(c.isalpha() for c in password)
        has_number = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)

        if password and not (has_letter and has_number and has_special):
            raise ValidationError("비밀번호는 영문, 숫자, 특수기호를 모두 포함해야 합니다.")

        return password2

    def save(self):
        # UserCreationForm의 save를 오버라이딩하는 대신, 직접 사용자를 생성합니다.
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = User.objects.create_user(username=username, password=password)
        return user

