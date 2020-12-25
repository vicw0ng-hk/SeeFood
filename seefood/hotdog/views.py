from django.shortcuts import render
from fastai.vision.all import load_learner
from pathlib import Path
from .forms import UploadFileForm
from random import randint


# Create your views here.
path = Path().cwd()/'hotdog'/'ml_model'
learn_inf = load_learner(path/'export.pkl')

def handle_uploaded_file(f):
    num = str(hex(randint(1000000000, 9999999999))[2:])
    my_file = Path().cwd()/'hotdog'/'static'/'images'/(num+'.upload')
    while my_file.is_file():
        num = str(hex(randint(1000000000, 9999999999))[2:])
        my_file = Path().cwd()/'hotdog'/'static'/'images'/(num+'.upload')
    filename = 'hotdog/static/images/' + num + '.upload'
    with open(filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return filename

def main(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            filename = handle_uploaded_file(request.FILES['file'])
            res = learn_inf.predict(filename)[0]
            context = {'res': res, 'file': filename.split('/')[-1]}
            return render(request, 'hotdog/result.html', context)
    static_path = Path().cwd()/'hotdog'/'static'/'images'
    for child in static_path.glob('*'):
        child.unlink()
    context = {'form': UploadFileForm()}
    return render(request, 'hotdog/index.html', context)
