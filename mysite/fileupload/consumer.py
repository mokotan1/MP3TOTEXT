import json
from channels.generic.websocket import AsyncWebsocketConsumer

class TranscriptionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.fileupload_id = self.scope["url_route"]["kwargs"]["fileupload_id"]
        self.group_name = f"fileupload_{self.fileupload_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def transcription_progress(self, event):
        """
        Celery 작업으로부터 진행 상황 업데이트를 받아 클라이언트에 전송합니다.
        """
        await self.send(text_data=json.dumps({
            "progress": event.get("progress", 0),
            "text": event.get("text", "")
        }))

    async def transcription_complete(self, event):
        """
        Celery 작업 완료 메시지를 받아 클라이언트에 최종 결과를 전송합니다.
        """
        await self.send(text_data=json.dumps({
            "progress": 100,
            "text": event.get("text", "")
        }))
