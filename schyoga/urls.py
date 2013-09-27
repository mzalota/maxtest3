#from django.conf.urls.defaults import *
from django.conf.urls import *

#from schyoga.views import list
from schyoga.views.studios import Profile

urlpatterns = patterns('schyoga.views',
    url(r'^site-map.html$', 'other.siteMap', name='site-map'),
    url(r'^shout-outs.html$', 'other.shoutOuts', name='shout-outs'),

    url(r'^events/', 'other.events'),

    url(r'^(?P<state_url_name>\S+)/studios/(?P<studio_url_name>\S+)/$', Profile.as_view(), name='studio-profile'),
    #url(r'^(?P<state_url_name>\S+)/studios/(?P<studio_url_name>\S+)/$', 'studios.profile', name='studio-profile'),
    url(r'^(?P<state_url_name>\S+)/studios/(?P<studio_url_name>\S+)/schedule.html$', 'studios.schedule', name='studio-schedule'),
    url(r'^(?P<state_url_name>\S+)/studios/(?P<studio_url_name>\S+)/facebook-feed.html$', 'studios.facebookFeed', name='studio-facebook-feed'),
    url(r'^(?P<state_url_name>\S+)/studios/', 'studios.list', name='studios'),

    url(r'^(?P<state_url_name>\S+)/teachers/(?P<teacher_url_name>\S+)/facebook-feed.html$', 'teachers.facebookFeed', name='teacher-facebook-feed'),
    url(r'^(?P<state_url_name>\S+)/teachers/(?P<teacher_url_name>\S+)/schedule.html$', 'teachers.schedule', name='teacher-schedule'),
    url(r'^(?P<state_url_name>\S+)/teachers/(?P<teacher_url_name>\S+)/$', 'teachers.profile', name='teacher-profile'),
    url(r'^(?P<state_url_name>\S+)/teachers/$', 'teachers.list', name='teachers'),

    #url(r'^(?P<state_url_name>\S+)/$', 'other.states', name='states'),

    url(r'^$', 'other.index', name='index'),
    #url(r'^$', archive),
)

