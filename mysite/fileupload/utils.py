import whisper
from django.conf import settings

_whisper_model = None
_whisper_device = None
_whisper_size = None

def get_whisper_model():
    """
    설정 파일에서 지정된 모델 크기 및 장치로 Whisper 모델을 로드하고 캐시합니다.
    """
    global _whisper_model, _whisper_device, _whisper_size

    current_device = getattr(settings, "WHISPER_DEVICE", "cpu")
    current_size = getattr(settings, "WHISPER_MODEL_SIZE", "base")

    if (
        _whisper_model is None
        or _whisper_device != current_device
        or _whisper_size != current_size
    ):
        print(f"Loading Whisper model: {current_size} on {current_device}")
        _whisper_model = whisper.load_model(name=current_size, device=current_device)
        _whisper_device = current_device
        _whisper_size = current_size

    return _whisper_model
