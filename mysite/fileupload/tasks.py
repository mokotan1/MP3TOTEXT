from celery import shared_task
from .models import FileUpload
from .utils import get_whisper_model
from django.core.exceptions import ObjectDoesNotExist

@shared_task
def transcribe_fileupload(fileupload_id: int):
    try:
        try:
            instance = FileUpload.objects.get(pk=fileupload_id)
        except ObjectDoesNotExist:
            print(f"[ERROR] FileUpload ID={fileupload_id} 존재하지 않음. 워커가 종료되지 않고 안전하게 리턴합니다.")
            return

        print(f"[DEBUG] 전사 시작: {instance.filename}") 

        model = get_whisper_model()
        result = model.transcribe(instance.file.path)

        instance.transcribed_txt = result.get("text", "")
        instance.save(update_fields=["transcribed_txt"])

        print(f"[DEBUG] 전사 완료: {instance.filename}") 
        print(f"[DEBUG] 전사 결과: {instance.transcribed_txt[:100]}...") 

        # WebSocket 알림
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"fileupload_{instance.pk}",
            {"type": "transcription.complete", "id": instance.pk, "text": instance.transcribed_txt},
        )
    except Exception as e:
        print(f"[ERROR] 전사 실패: {e}") 
        raise e