# fileupload/consumers.py

import json
from channels.generic.websocket import WebsocketConsumer

class TranscriptionConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        # 연결이 성공하면 클라이언트에게 메시지 전송
        self.send(text_data=json.dumps({
            'message': 'Connected to transcription service.'
        }))

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        # 클라이언트로부터 메시지를 받을 때 실행
        data = json.loads(text_data)
        if data['type'] == 'start_transcription':
            # 여기서 전사 작업을 시작하는 Celery 태스크를 호출
            # (예: transcribe_task.delay(data['file_path'], self.channel_name))
            
            # 클라이언트에게 작업 시작 메시지 전송
            self.send(text_data=json.dumps({
                'status': 'started',
                'message': 'Transcription started.'
            }))

            # 실제 전사 로직은 여기에 넣지 않고,
            # 별도의 비동기 태스크에서 진행 상황을 이 채널로 다시 보냅니다.
            # 예시:
            # self.send(text_data=json.dumps({
            #     'status': 'progress',
            #     'percentage': 50
            # }))
            # self.send(text_data=json.dumps({
            #     'status': 'completed',
            #     'result': '전사된 텍스트'
            # }))