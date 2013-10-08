#from django.conf.urls.defaults import *
from django.conf.urls import *

#from schyoga.views import list
from django.views.generic import TemplateView
from schyoga.views.studios import Profile

urlpatterns = patterns('schyoga.views',

    #url(r'^favicon.ico$', TemplateView.as_view(template_name="favicon.ico"), name='favicon'),

    url(r'^about-us.html$', TemplateView.as_view(template_name="about-us.html"), name='about-us'),
    url(r'^privacy-policy.html$', TemplateView.as_view(template_name="privacy-policy.html"), name='privacy-policy'),

    url(r'^site-map.html$', 'other.siteMap', name='site-map'),
    url(r'^shout-outs.html$', 'other.shoutOuts', name='shout-outs'),

    url(r'^error404.html$', TemplateView.as_view(template_name="404.html"), name='error404'),
    url(r'^error500.html$', TemplateView.as_view(template_name="500.html"), name='error500'),

    #url(r'^(?P<state_url_name>\S+)/studios/(?P<studio_url_name>\S+)/$', 'studios.profile', name='studio-profile'),
    url(r'^(?P<state_url_name>\S+)/studios/(?P<studio_url_name>\S+)/schedule.html$', 'studios.schedule', name='studio-schedule'),
    url(r'^(?P<state_url_name>\S+)/studios/(?P<studio_url_name>\S+)/facebook-feed.html$', 'studios.facebookFeed', name='studio-facebook-feed'),
    url(r'^(?P<state_url_name>\S+)/studios/(?P<studio_url_name>\S+)/(?P<year>\S+)-(?P<month>\S+)-(?P<day>\S+).html$', 'studios.schedule_one_day', name='studio-one-day-schedule'),
    url(r'^(?P<state_url_name>\S+)/studios/(?P<studio_url_name>\S+)/$', Profile.as_view(), name='studio-profile'),
    url(r'^(?P<state_url_name>\S+)/studios/', 'studios.list', name='studios'),

    url(r'^(?P<state_url_name>\S+)/teachers/(?P<teacher_url_name>\S+)/facebook-feed.html$', 'teachers.facebookFeed', name='teacher-facebook-feed'),
    url(r'^(?P<state_url_name>\S+)/teachers/(?P<teacher_url_name>\S+)/schedule.html$', 'teachers.schedule', name='teacher-schedule'),
    url(r'^(?P<state_url_name>\S+)/teachers/(?P<teacher_url_name>\S+)/$', 'teachers.profile', name='teacher-profile'),
    url(r'^(?P<state_url_name>\S+)/teachers/$', 'teachers.list', name='teachers'),

    url(r'^(?P<state_url_name>\S+)/$', 'other.states', name='states'),

    url(r'^$', 'other.index', name='index'),
)

