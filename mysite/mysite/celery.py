from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings  # Django settings를 import합니다.

# Django 프로젝트의 settings 파일을 Celery의 환경 변수로 설정합니다.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

# 'mysite'라는 이름의 Celery 애플리케이션을 생성합니다.
app = Celery("mysite")

# Django settings의 CELERY_* 설정을 Celery에 적용합니다.
# `settings` 네임스페이스를 사용하면 CELERY_로 시작하는 모든 설정 키가 자동으로 적용됩니다.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Django 앱의 tasks.py 파일을 자동으로 탐색합니다.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
