from django.conf.urls import url
from . import views

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/new/$', views.post_new, name='post_new'),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns() + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)