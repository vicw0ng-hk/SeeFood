from django.shortcuts import render
from fastai.vision.all import load_learner
from pathlib import Path
from .forms import UploadFileForm
from django.conf import settings
from .models import *
from datetime import datetime, timedelta, timezone


# Create your views here.
path = Path(settings.STATIC_ROOT)/'ml_model'
learn_inf = load_learner(path/'export.pkl')

def main(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            res = learn_inf.predict(Path(settings.MEDIA_ROOT + obj.file.name))[0]
            context = {'res': res, 'file': obj.file.url}
            return render(request, 'hotdog/result.html', context)
        else:
            context = {'form': UploadFileForm(), 'message': 'File Not Supported!'}
            return render(request, 'hotdog/index.html', context)
    for image in Image.objects.all():
        if datetime.now(timezone.utc) - image.time > timedelta(minutes=3):
            Path(settings.MEDIA_ROOT + image.file.name).unlink(missing_ok=True)
            image.delete()
    context = {'form': UploadFileForm()}
    return render(request, 'hotdog/index.html', context)
