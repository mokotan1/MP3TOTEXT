from django.shortcuts import redirect, render
from .forms import fileUploadForm
from .models import fileupload
from django.conf import settings

def upload_file(request):
    # 업로드된 파일을 미리 확인
    upload_files = fileupload.objects.all()

    form = fileUploadForm()

    if request.method == "POST":
        form = fileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_file')
        else: 
            form = fileUploadForm()

    return render(request, 'fileupload/fileupload.html', 
    {
        'form': form,
        'upload_files': upload_files,
    })

    