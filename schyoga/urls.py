#from django.conf.urls.defaults import *
from django.conf.urls import *

#from schyoga.views import list


urlpatterns = patterns('schyoga.views',
    url(r'^events/', 'other.events'),

    url(r'^studios/(?P<state_url_name>\S+)/(?P<studio_url_name>\S+)/$', 'studios.profile', name='studio-profile'),
    url(r'^studios/(?P<state_url_name>\S+)/(?P<studio_url_name>\S+)/schedule.html$', 'studios.schedule', name='studio-schedule'),
    url(r'^studios/(?P<state_url_name>\S+)/(?P<studio_url_name>\S+)/facebook-feed.html$', 'studios.facebookFeed', name='studio-facebook-feed'),
    url(r'^studios/(?P<state_url_name>\S+)/', 'studios.list', name='studios'),

    url(r'^teachers/(?P<state_url_name>\S+)/(?P<teacher_url_name>\S+)/facebook-feed.html$', 'teachers.facebookFeed', name='teacher-facebook-feed'),
    url(r'^teachers/(?P<state_url_name>\S+)/(?P<teacher_url_name>\S+)/schedule.html$', 'teachers.schedule', name='teacher-schedule'),
    url(r'^teachers/(?P<state_url_name>\S+)/(?P<teacher_url_name>\S+)/$', 'teachers.profile', name='teacher-profile'),
    url(r'^teachers/(?P<state_url_name>\S+)/$', 'teachers.list', name='teachers'),

    url(r'^site-map.html$', 'other.siteMap', name='site-map'),
    url(r'^shout-outs.html$', 'other.shoutOuts', name='shout-outs'),
    #url(r'^$', archive),
)

