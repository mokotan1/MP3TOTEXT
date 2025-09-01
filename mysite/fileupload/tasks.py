from celery import shared_task
from .models import FileUpload
from .utils import get_whisper_model

@shared_task
def transcribe_fileupload(fileupload_id: int):
    instance = FileUpload.objects.get(pk=fileupload_id)
    model = get_whisper_model()
    result = model.transcribe(instance.file.path)
    instance.transcribed_txt = result.get("text", "")
    instance.save(update_fields=["transcribed_txt"])

    from channels.layers import get_channel_layer
    from asgiref.sync import async_to_sync

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"fileupload_{instance.pk}",
        {"type": "transcription.complete", "id": instance.pk, "text": instance.transcribed_txt},
    )