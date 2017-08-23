from django.conf.urls import url
from . import views

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^upload/$', views.model_form_upload, name='model_form_upload'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^start/$', views.post_start, name='post_start'),
    url(r'^stop/$', views.post_stop, name='post_stop'),
    url(r'^post/new/$', views.post_new, name='post_new'),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns() + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)