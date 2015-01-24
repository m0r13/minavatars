from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r"^head/(?P<user>[a-zA-Z0-9-_]+)$", views.head, {"size" : 1}, name="head"),
    url(r"^head/(?P<user>[a-zA-Z0-9-_]+)/(?P<size>\d+)$", views.head, name="head"),
    
    url(r"^body/(?P<user>[a-zA-Z0-9-_]+)$", views.body, {"size" : 1}, name="body"),
    url(r"^body/(?P<user>[a-zA-Z0-9-_]+)/(?P<size>\d+)$", views.body, name="body"),
)
