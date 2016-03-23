from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings


urlpatterns = patterns('',

    url(r'^$', 'rango.views.index', name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rango/', include('rango.urls')),
    url(r'^accounts/login/', 'rango.views.user_login', name='login' )
    
)

# From https://stackoverflow.com/questions/5517950/django-media-url-and-media-root
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))