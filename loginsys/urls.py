from django.conf.urls import url
from loginsys.views import logout, login


urlpatterns = [
    url(r'^login/', login, name='login'),
    url(r'^logout/', logout, name='logout'),
]