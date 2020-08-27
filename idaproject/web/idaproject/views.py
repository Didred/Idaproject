from django.shortcuts import render
from django.shortcuts import (
    render,
    redirect
)
from . import get_api
from .forms import PictureForm, ShowForm

def home(request):
    api = get_api()
    pictures = api.get_pictures()

    return render(request, 'home.html', {'pictures': pictures})

def add(request):
    api = get_api()

    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES)
        if form.is_valid():
            picture = request.FILES['file'].file.getvalue() if request.FILES else None
            link = form.cleaned_data['link']

            if (picture and link) or (not picture and not link):
                return render(request, 'add.html', {'form': PictureForm, 'errors': 'Не введено ни одного варианта, или введены оба'})

            name = request.FILES['file'].name if picture else "test"
            try:
                id = api.add(link, name, picture)
            except:
                return render(request, 'add.html', {'form': PictureForm, 'errors': "Невалидная ссылка"})

            return redirect('/get/' + str(id))
    return render(request, 'add.html', {'form': PictureForm})

def get(request, id):
    api = get_api()

    if request.method == 'POST':
        form = ShowForm(request.POST)
        print()
        if form.is_valid():
            width = form.cleaned_data['width']
            height = form.cleaned_data['height']
            image = api.resize(id, width, height)
            picture = str(image.picture)[2: -1]

            return render(request, 'get.html', {'image': image, 'picture': picture, 'form': form})

    else:
        form = ShowForm()

    image = api.get(id)
    picture = api.convert_picture(image.picture)
    return render(request, 'get.html', {'image': image, 'picture': picture, 'form': form})

