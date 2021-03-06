#from django.conf.urls.defaults import *
#from django.conf.urls import *

from django.conf.urls import patterns, include, url

from django.contrib import admin
from schyoga.views.teachers import TeacherViews

admin.autodiscover()

#from schyoga.views import list
from django.views.generic import TemplateView, RedirectView
from schyoga.bizobj.page import Page
from schyoga.views.studios import StudioViews

#TODO: V.2. add a sitemap
#TODO: Test how the page schedule looks with IE 9 (make sure Top Nav menu is not wierd)
#TODO: Figure out why this URL is not working: http://127.0.0.1:8000/new-york/studios/bikram-yoga-grand-central/2013-10-08.html/

urlpatterns = patterns('schyoga.views',

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    #url(r'^favicon.ico$', TemplateView.as_view(template_name="favicon.ico"), name='favicon'),

    url(r'^robots.txt$', TemplateView.as_view(template_name="robots.txt", content_type='text/plain'), name='robots'),

    url(r'^BingSiteAuth.xml', TemplateView.as_view(template_name="BingSiteAuth.xml", content_type='text/xml'), name='bing-site-auth'),

    url(r'^about-us.html$', TemplateView.as_view(template_name="about-us.html"), name='about-us'),
    url(r'^privacy-policy.html$', TemplateView.as_view(template_name="privacy-policy.html"), name='privacy-policy'),

    url(r'^site-map.html$', 'other.siteMap', name='site-map'),
    url(r'^shout-outs.html$', 'other.shoutOuts', name='shout-outs'),

    url(r'^error404.html$', TemplateView.as_view(template_name="404.html"), name='error404'),
    url(r'^error500.html$', TemplateView.as_view(template_name="500.html"), name='error500'),

    #fixing a spelling error that existed for 2.5 years. It should have been Baptiste instead of Babtiste
    url(r'^massachusetts/studios/babtiste(?P<the_rest_of_url>\S+)$', RedirectView.as_view(url='/massachusetts/studios/baptiste%(the_rest_of_url)s')),

    url(r'^studios/new-york(?P<the_rest_of_url>\S+)$', RedirectView.as_view(url='/new-york/studios%(the_rest_of_url)s')),
    url(r'^studios/connecticut(?P<the_rest_of_url>\S+)$', RedirectView.as_view(url='/connecticut/studios%(the_rest_of_url)s')),
    url(r'^studios/massachusetts(?P<the_rest_of_url>\S+)$', RedirectView.as_view(url='/massachusetts/studios%(the_rest_of_url)s')),
    url(r'^studios/...(?P<the_rest_of_url>\S+)$', RedirectView.as_view(url='/new-york/studios%(the_rest_of_url)s')),

    url(r'^teachers/new-york(?P<the_rest_of_url>\S+)$', RedirectView.as_view(url='/new-york/teachers%(the_rest_of_url)s')),
    url(r'^teachers/connecticut(?P<the_rest_of_url>\S+)$', RedirectView.as_view(url='/connecticut/teachers%(the_rest_of_url)s')),
    url(r'^teachers/massachusetts(?P<the_rest_of_url>\S+)$', RedirectView.as_view(url='/massachusetts/teachers%(the_rest_of_url)s')),
    url(r'^teachers/...(?P<the_rest_of_url>\S+)$', RedirectView.as_view(url='/new-york/teachers%(the_rest_of_url)s')),

    url(r'^(?P<state_url_name>\S+)/studios/(?P<studio_url_name>\S+)/schedule.html$', StudioViews.as_view(pagename=Page.ENUM_STUDIO_SCHEDULE), name='studio-schedule'), #'studios.schedule'
    url(r'^(?P<state_url_name>\S+)/studios/(?P<studio_url_name>\S+)/facebook-feed.html$', StudioViews.as_view(pagename=Page.ENUM_STUDIO_FACEBOOKFEED), name='studio-facebook-feed'),
    url(r'^(?P<state_url_name>\S+)/studios/(?P<studio_url_name>\S+)/(?P<year>\S+)-(?P<month>\S+)-(?P<day>\S+).html$', 'studios.schedule_one_day', name='studio-one-day-schedule'),
    url(r'^(?P<state_url_name>\S+)/studios/(?P<studio_url_name>\S+)/$', StudioViews.as_view(pagename=Page.ENUM_STUDIO_PROFILE), name='studio-profile'),
    url(r'^(?P<state_url_name>\S+)/studios/', 'studios.list', name='studios'),

    url(r'^(?P<state_url_name>\S+)/teachers/(?P<teacher_url_name>\S+)/next-week.html$', RedirectView.as_view(url='/%(state_url_name)s/teachers/%(teacher_url_name)s/schedule.html'), name='teacher-next-week'),
    url(r'^(?P<state_url_name>\S+)/teachers/(?P<teacher_url_name>\S+)/facebook-feed.html$', TeacherViews.as_view(pagename=Page.ENUM_TEACHER_FACEBOOKFEED), name='teacher-facebook-feed'),
    url(r'^(?P<state_url_name>\S+)/teachers/(?P<teacher_url_name>\S+)/schedule.html$', TeacherViews.as_view(pagename=Page.ENUM_TEACHER_SCHEDULE), name='teacher-schedule'),
    url(r'^(?P<state_url_name>\S+)/teachers/(?P<teacher_url_name>\S+)/feedback-received.html$',TemplateView.as_view(template_name="teacher/feedback-received.html"), name='teacher-feedback-received'),
    url(r'^(?P<state_url_name>\S+)/teachers/(?P<teacher_url_name>\S+)/$', TeacherViews.as_view(pagename=Page.ENUM_TEACHER_PROFILE), name='teacher-profile'),
    url(r'^(?P<state_url_name>\S+)/teachers/$', 'teachers.list', name='teachers'),

    url(r'^(?P<state_url_name>\S+)/$', 'other.states', name='states'),

    url(r'^$', 'other.index', name='index'),
)

