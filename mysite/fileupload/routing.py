from django.urls import re_path
from . import consumer

websocket_urlpatterns = [
    re_path(r'ws/fileupload/(?P<fileupload_id>\\d+)/$', consumer.TranscriptionConsumer.as_asgi()),
]
