from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^loginview$', views.loginview),
    url(r'^login$', views.login),
    url(r'^registration$', views.registration),
    url(r'^home$', views.home),
    url(r'^add_postit$', views.add_postit),
    url(r'^like/(?P<id>\d+)$', views.like_message),
    url(r'^details/(?P<id>\d+)$', views.details),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^logout$', views.logout),
]