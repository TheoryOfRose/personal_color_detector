from django.db import models


class Photo(models.Model):
    file = models.ImageField()
    color1 = models.CharField(max_length=255, blank=True)
    color2 = models.CharField(max_length=255, blank=True)
    first = models.IntegerField(default=0)
    question1 = models.IntegerField(default=0)
    question2 = models.IntegerField(default=0)
    question3 = models.IntegerField(default=0)
    question4 = models.IntegerField(default=0)
    #personal_color = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = 'photo'
        verbose_name_plural = 'photos'
