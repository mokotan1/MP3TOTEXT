from celery import shared_task
from .models import FileUpload
from .utils import get_whisper_model
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import math
import librosa
import numpy as np
import os # Import the os module

@shared_task
def transcribe_fileupload(fileupload_id: int):
    try:
        instance = FileUpload.objects.get(pk=fileupload_id)
        model = get_whisper_model()
        audio_path = instance.file.path

        audio, sr = librosa.load(audio_path, sr=None)
        
        # Whisper model expects 16kHz
        if sr != 16000:
            audio = librosa.resample(audio, orig_sr=sr, target_sr=16000)
            sr = 16000

        total_frames = len(audio)
        chunk_size = sr * 30 # Optimized for 30-second chunks

        transcribed_text = ""
        channel_layer = get_channel_layer()

        for i in range(0, total_frames, chunk_size):
            chunk = audio[i:i+chunk_size]
            
            # Use the transcribe method which returns segments
            result = model.transcribe(chunk)
            
            # Join segments with a newline character to create line breaks
            segments = result.get("segments", [])
            for segment in segments:
                transcribed_text += segment.get("text", "") + "\n"

            progress = min(100, math.ceil((i + chunk_size) / total_frames * 100))

            async_to_sync(channel_layer.group_send)(
                f"fileupload_{instance.pk}",
                {
                    "type": "transcription.progress",
                    "id": instance.pk,
                    "progress": progress,
                    "text": transcribed_text
                }
            )

        instance.transcribed_txt = transcribed_text
        instance.save(update_fields=["transcribed_txt"])

        async_to_sync(channel_layer.group_send)(
            f"fileupload_{instance.pk}",
            {
                "type": "transcription.complete",
                "id": instance.pk,
                "text": transcribed_text
            }
        )

    except FileUpload.DoesNotExist:
        print(f"FileUpload with id {fileupload_id} not found.")
    except Exception as e:
        print(f"An error occurred during transcription: {e}")
