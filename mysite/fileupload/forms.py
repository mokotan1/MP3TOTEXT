from django import forms
from .models import fileupload

class fileUploadForm(forms.ModelForm):
    class Meta:
        model = fileupload
        fields = {'file', 'description'}