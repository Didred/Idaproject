from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^add$', views.add, name='add'),
    url(r'^get/(?P<id>[0-9]+)$', views.get, name='get'),
]