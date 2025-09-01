from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/transcription/(?P<fileupload_id>\\d+)/$", consumers.TranscriptionConsumer.as_asgi()),
]
