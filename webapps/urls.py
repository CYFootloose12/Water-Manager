from django.conf.urls import patterns, include, url
import watermanager

urlpatterns = patterns('',
    url(r'', include('watermanager.urls')),
)
