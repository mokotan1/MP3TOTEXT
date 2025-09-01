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

    async def transcription_complete(self, event):
        await self.send(text_data=json.dumps({
            "id": event["id"],
            "text": event["text"]
        }))