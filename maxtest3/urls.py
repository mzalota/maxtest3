from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#handler404 = 'schyoga.views.other.page404'

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'maxtest3.views.home', name='home'),
    # url(r'^maxtest3/', include('maxtest3.foo.urls')),



    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^', include('schyoga.urls')),
)
