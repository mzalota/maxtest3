#from django.conf.urls.defaults import *
from django.conf.urls import *

#from schyoga.views import instructors


urlpatterns = patterns('schyoga.views',
    url(r'^events/', 'other.events'),
    url(r'^studios/', 'studios.list', name = 'studios'),
    url(r'^instructors/(?P<instructor_url_name>\S+)/facebook-feed.html$', 'instructors.instructorFacebookFeed', name='instructor-facebook-feed'),
    url(r'^instructors/(?P<instructor_url_name>\S+)/schedule.html$', 'instructors.instructorSchedule', name='instructor-schedule'),
    url(r'^instructors/(?P<instructor_url_name>\S+)/$', 'instructors.instructor', name='instructor'),
    url(r'^instructors/$', 'instructors.instructors', name='instructors'),
    url(r'^site-map.html$', 'other.siteMap', name='site-map'),
    url(r'^shout-outs.html$', 'other.shoutOuts', name='shout-outs'),
    #url(r'^$', archive),
)

