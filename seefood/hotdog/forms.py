from django import forms
from .models import *


class UploadFileForm(forms.ModelForm):
    file = forms.ImageField()

    class Meta:
        model = Image
        fields = ['file']