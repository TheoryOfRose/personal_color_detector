from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from mysite.album import views


urlpatterns = [
    url(r'^result/$', views.photo_result, name='photo_result'),
    url(r'^$', views.photo_home, name='photo_home'),
    url(r'^survey/$', views.photo_survey, name='photo_survey'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
