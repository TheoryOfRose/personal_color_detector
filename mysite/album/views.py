from django.shortcuts import render, redirect

from .models import Photo
from .forms import PhotoForm


def photo_result(request):
    photos = Photo.objects.all()
    print(photos[0].color1)
    print(photos[0].color2)
    """if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('photo_list')
    else:
        form = PhotoForm()"""
    form = PhotoForm()
    return render(request, 'album/photo_result.html', {'form': form, 'photos': photos})

def photo_home(request):
    #Photo.objects.all().delete()
    #photos = Photo.objects.all()
    #form = PhotoForm()
    #return render(request, 'album/photo_reset.html', {'form': form, 'photos': photos})
    
    if request.method == 'POST':
        #Photo.objects.all().delete()
        photos = Photo.objects.all()
        print(request.POST, request.FILES)
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(True, "","")
            return redirect('photo_survey')
    else:
        Photo.objects.all().delete()
        photos = Photo.objects.all()
        form = PhotoForm()
    return render(request, 'album/photo_home.html', {'form': form, 'photos': photos})

def photo_survey(request):
    #Photo.objects.all().delete()
    
    if request.method == 'POST':
        q1 = int(request.POST['q1'])
        q2 = int(request.POST['q2'])
        q3 = int(request.POST['q3'])
        q4 = int(request.POST['q4'])
        print(q1, q2, q3, q4)
        color2 = ""
        if q1+q2+q3 >= 2:
            if q4 == 1:
                color2 = "spring_warm"
            else:
                color2 = "autumn_warm"
        else:
            if q4 == 1:
                color2 = "summer_cool"
            else:
                color2 = "winter_cool"

        photos = Photo.objects.all()
        color1 = photos[0].color1
        req = {'x': 0.0, 'y': 0.0, 'height': 0.0, 'width': 0.0}
        f = {'file': photos[0].file }
        Photo.objects.all().delete()
        form = PhotoForm(req, f)
        form.save(False,color1,color2)

        return redirect('photo_result')
    
    return render(request, 'album/photo_survey.html')