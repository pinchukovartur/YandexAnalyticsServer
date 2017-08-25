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
    url(r'^delete/$', views.post_delete, name='post_delete'),
    url(r'^update/$', views.post_update, name='post_update'),
    url(r'^cpu/$', views.get_cpu_info, name='get_cpu_info'),
    url(r'^memory/$', views.get_memory_info, name='get_memory_info'),
    url(r'^disk/$', views.get_disk_info, name='get_disk_info'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^start_download/(?P<status_code>[a-z]+)/$$', views.post_start_insert_in_db, name='post_start_insert_in_db'),

]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns() + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)