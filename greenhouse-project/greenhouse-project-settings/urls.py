from django.conf import settings
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'', include('greenhouse.urls')),
)

if settings.STATIC_SERVE:
    urlpatterns += patterns('',
                            url(r'^media/(?P<path>.*)$',
                                'django.views.static.serve',
                                {'document_root': settings.MEDIA_ROOT}),
                            )
