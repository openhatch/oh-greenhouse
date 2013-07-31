from django.conf import settings
from django.conf.urls import patterns, include, url
from uploads import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'contributors.views.home', name='home'),
    # url(r'^contributors/', include('devtracking.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^openid/', include('django_openid_auth.urls')),
    url(r'^logout$', views.site_logout, name='logout'),
    url(r'^denied(.+)', views.access_denied, name='denied'),
    url(r'^$', views.index, name='home'),
    url(r'^contributors/first_timers', views.first_timers, name='first_timers'),
    url(r'^contributors/recent_contributors', views.recent_contributors, name='recent_contributors'),
    url(r'^contributors/lost_contributors', views.lost_contributors, name='lost_contributors'),
    url(r'^contributors/potential_devs', views.potential_devs, name='potential_devs'),
    url(r'^contacted/(?P<email>.+)', views.contacted, name='contacted'),
    url(r'^contributors/(?P<email>.+)/edit', views.edit_person, name='edit_person'),
    url(r'^contributors/(?P<email>.+)', views.person_detail, name='person_detail'),
    url(r'^users/(?P<user>.+)', views.user_profile, name='user_profile'),
    url(r'^delete_comment/(?P<email>.+)/(?P<comment_id>.+)', views.delete_comment, name='delete_comment'),
    url(r'^unify', views.unify_identities, name='unify_identities'), 
    url(r'^comments/', include('django.contrib.comments.urls'))
)

if settings.STATIC_SERVE:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
