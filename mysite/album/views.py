from django.shortcuts import render, redirect

from .models import Photo
from .forms import PhotoForm


def photo_list(request):
    photos = Photo.objects.all()
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('photo_list')
    else:
        form = PhotoForm()
    return render(request, 'album/photo_list.html', {'form': form, 'photos': photos})

def photo_reset(request):
    #Photo.objects.all().delete()
    #photos = Photo.objects.all()
    #form = PhotoForm()
    #return render(request, 'album/photo_reset.html', {'form': form, 'photos': photos})
    
    if request.method == 'POST':
        #Photo.objects.all().delete()
        photos = Photo.objects.all()
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('photo_list')
    else:
        Photo.objects.all().delete()
        photos = Photo.objects.all()
        form = PhotoForm()
    return render(request, 'album/photo_reset.html', {'form': form, 'photos': photos})