from django.conf.urls.defaults import *
#from schyoga.views import instructors
from schyoga.views import jeanneHeaton
from schyoga.views import events
from schyoga.views import studios
from schyoga.views import siteMap
from schyoga.views import shoutOuts

urlpatterns = patterns('schyoga.views',
    url(r'^events/', events),
    url(r'^studios/', studios, name = 'studios'),
    url(r'^instructors/(?P<instructor_url_name>\S+)/$', jeanneHeaton, name='instructor'),
    url(r'^instructors/$', 'instructors', name='instructors'),
    url(r'^site-map.html$', siteMap, name='site-map'),
    url(r'^shout-outs.html$', shoutOuts, name='shout-outs'),
    #url(r'^$', archive),
)