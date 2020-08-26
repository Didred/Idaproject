from django import forms
from PIL import Image


class PictureForm(forms.Form):
    link = forms.CharField(max_length=1000, required=False)
    file = forms.ImageField(required=False)

class ShowForm(forms.Form):
    width = forms.CharField(max_length=100, required=True)
    height = forms.CharField(max_length=100, required=True)