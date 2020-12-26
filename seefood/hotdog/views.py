from django.shortcuts import render
from fastai.vision.all import load_learner
from pathlib import Path
from .forms import UploadFileForm
from django.conf import settings
from .models import *
from datetime import datetime, timedelta, timezone
import os


# Create your views here.
path = Path().cwd()/'hotdog'/'ml_model'
learn_inf = load_learner(path/'export.pkl')

def main(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            file = settings.MEDIA_ROOT + '/' + obj.file.name
            res = learn_inf.predict(file)[0]
            context = {'res': res, 'file': obj.file.url}
            return render(request, 'hotdog/result.html', context)
        else:
            context = {'form': UploadFileForm(), 'message': 'File Not Supported!'}
            return render(request, 'hotdog/index.html', context)
    for image in Image.objects.all():
        if datetime.now(timezone.utc) - image.time > timedelta(minutes=3):
            os.remove(settings.MEDIA_ROOT + '/' + image.file.name)
            image.delete()
    context = {'form': UploadFileForm()}
    return render(request, 'hotdog/index.html', context)
