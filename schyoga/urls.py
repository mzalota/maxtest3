#from django.conf.urls.defaults import *
from django.conf.urls import *

#from schyoga.views import instructors


urlpatterns = patterns('schyoga.views',
    url(r'^events/', 'events'),
    url(r'^studios/', 'studios', name = 'studios'),
    url(r'^instructors/(?P<instructor_url_name>\S+)/schedule.html$', 'instructorSchedule', name='instructor-schedule'),
    url(r'^instructors/(?P<instructor_url_name>\S+)/$', 'instructor', name='instructor'),
    url(r'^instructors/$', 'instructors', name='instructors'),
    url(r'^site-map.html$', 'siteMap', name='site-map'),
    url(r'^shout-outs.html$', 'shoutOuts', name='shout-outs'),
    #url(r'^$', archive),
)