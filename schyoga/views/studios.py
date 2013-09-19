from django.template import loader, Context, RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response

from schyoga.models import Instructor
from schyoga.models import Studio
from schyoga.models import Event


#import collections
#import datetime
#import facebook


def list(request):
    studios = Studio.objects.all()
    #t = loader.get_template("studios.html")
    #c = Context({'studios': studios})
    #return HttpResponse(t.render(c))
    return render_to_response('studios.html',
                            { 'studios': studios, },
                            context_instance=RequestContext(request))