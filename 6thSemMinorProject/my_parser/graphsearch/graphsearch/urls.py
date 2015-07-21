from django.conf.urls import patterns, include, url
from graphsearch.views import *
urlpatterns = patterns('',
    url(r'^$', home),
    url(r'^oauth/$', oauth),
    url(r'^oauth_callback/$', oauth_callback),
    url(r'^myapp/$', mainapp),
    url(r'^processQuery/$', processQuery),
)
