# Create your views here.

from django.template import loader, Context, RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response

from schyoga.models import Instructor
from schyoga.models import Studio
from schyoga.models import Event


import collections
import datetime

import facebook


def siteMap(request):
    return render_to_response('site-map.html', {}, RequestContext(request))


def shoutOuts(request):
    return render_to_response('shout-outs.html', {}, RequestContext(request))


def events(request):
    #today = datetime.date.today()
    #cutoff = (today - datetime.timedelta(days=30))
    #events = Event.objects.filter(timestamp__lt=cutoff)
    events = Event.objects.filter(instructor_name = 'Abby')

    t = loader.get_template("events.html")
    c = Context({ 'events': events})
    return HttpResponse(t.render(c))




 #def friends(request):
     #django_facebook.middleware.FacebookMiddleware.get_fb_user()
     # if request.facebook:
 #       friends = request.facebook.graph.get_connections('me', 'friends')


#<img src="{% static "my_app/myexample.jpg" %}" alt="My image"/>