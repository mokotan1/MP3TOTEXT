import whisper
from django.conf import settings
_whisper_model = None 
_whisper_device = None
_whisper_size = None

def get_whisper_model():
    global _whisper_model, _whisper_device, _whisper_size
    
    current_device = settings.WHISPER_DEVICE
    current_size = settings.WHISPER_MODEL_SIZE
    if(_whisper_model is None or _whisper_device != current_device or  _whisper_size != current_size):
        _whisper_model = whisper.load_model(name= current_size , device=  current_device)
        _whisper_device = current_device
        _whisper_size = current_size
    return _whisper_model
   
