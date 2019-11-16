from PIL import Image

from django import forms
from django.core.files import File

from .models import Photo

import numpy as np
import cv2
import argparse
import mysite.album.skin_tone as skin_tone
import mysite.album.face_object as face_object
import mysite.album.lighting_removal as lighting_removal
import imutils
from matplotlib import pyplot as plt

class PhotoForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Photo
        fields = ('file', 'x', 'y', 'width', 'height', )
        widgets = {
            'file': forms.FileInput(attrs={
                'accept': 'image/*'  # this is not an actual validation! don't rely on that!
            })
        }

    def save(self):
        
        photo = super(PhotoForm, self).save()
        
        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        #photo = PhotoForm(**self.)

        image = Image.open(photo.file)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        resized_image.save(photo.file.path)

        image = cv2.imread(photo.file.path, cv2.IMREAD_COLOR)
        image = cv2.resize(image, dsize=(295,354), interpolation=cv2.INTER_AREA)
        preprocessing = lighting_removal.normalize(image,128)

        # Crop face and remove face objects
        face = face_object.extractFaceSkin(image)

        # Apply Skin Mask
        skin = skin_tone.extractSkin(image)
        result = cv2.bitwise_and(skin, face)

        dominantColors = skin_tone.extractDominantColor(lighting_removal.normalize(result,180), hasThresholding=True)
        dominantColorsForShowing = skin_tone.extractDominantColor(result, hasThresholding=True)
        rgb = dominantColors[0]['color']
        print(rgb)
        skin_color = np.zeros((1,1,3), np.uint8)
        print(skin_color)
        skin_color[0][0][0] = rgb[0]
        skin_color[0][0][1] = rgb[1]
        skin_color[0][0][2] = rgb[2]
        skin_color_lab = cv2.cvtColor(skin_color,cv2.COLOR_RGB2LAB)

        plt.figure(1, figsize=(4,1.5))
        plt.subplot(1, 3, 1)
        plt.axis("off")
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.title("Original Image", position=(0.5, 1.0+0.05), fontsize=10)

        colour_bar = skin_tone.plotColorBar(dominantColorsForShowing)
        plt.subplot(1, 3, 2)
        plt.axis("off")
        plt.imshow(colour_bar)
        plt.title("Color Bar", position=(0.5, 1.0+1.95), fontsize=10)

        textstr1 = '\n'.join((
        #r'Dominant Skin Color',
        r'$L = %.2f$' % (skin_color_lab.item(0,0,0), ),
        r'$A = %.2f$' % (skin_color_lab.item(0,0,1) - 128, ),
        r'$B = %.2f$' % (skin_color_lab.item(0,0,2) - 128, )))

        props = dict(boxstyle='round', facecolor='white', alpha=0.5)
        plt.subplot(1 ,3, 3)
        plt.axis("off")
        plt.text(0.2, 0.5, textstr1, fontsize=8, verticalalignment='center', bbox=props)
        plt.title("Skin Color", position=(0.5, 1.0+0.05), fontsize=10)

        plt.tight_layout()
        plt.savefig(photo.file.path,dpi=300)
        #cv2.imwrite(photo.file.path, blur)

        photo.description = "winter_cool"
        photo.save()

        return photo

