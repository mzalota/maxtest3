from django.template import loader, Context, RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response

#from schyoga.models import Instructor
from schyoga.models import Studio
#from schyoga.models import Event

from schyoga.bizobj.schedule import Schedule

import datetime
import facebook

#TODO: Need to provide state_url_name variable in every page so that top-level menus would work properly

def list(request, state_url_name):
    studios = Studio.objects.all()
    #t = loader.get_template("list.html")
    #c = Context({'studios': studios})
    #return HttpResponse(t.render(c))
    return render_to_response('studio/list.html',
                            { 'studios': studios,
                              'state_url_name': state_url_name, },
                            context_instance=RequestContext(request))

def profile(request, state_url_name, studio_url_name):

    studios = Studio.objects.filter(name_url=studio_url_name)
    studio = studios[0]

    return render_to_response('studio/studio-profile.html',
                          { 'studio': studio,},
                            RequestContext(request))


def schedule(request, state_url_name, studio_url_name):
    studios = Studio.objects.filter(name_url=studio_url_name)
    studio = studios[0]
    eventsTmp = studio.event_set.all().order_by('start_time')

    sched = Schedule(eventsTmp, datetime.datetime(2013, 8, 6), 14)

    return render_to_response('studio/schedule.html',
                                {'studio': studio,
                                 'calendar': sched, },
                              RequestContext(request))

def facebookFeed(request, state_url_name, studio_url_name):
    #https://www.facebook.com/JeanneEllenHeaton
    #https://graph.facebook.com/JeanneEllenHeaton/feed?access_token=CAAAAAITEghMBAIeRlyE803IvUcjjQ43WPkM44b36XLAnCVZBFjJEF76ZBBXaiDS7kBfSY4fqrEphDiXVZBl9ot9WFGZBCKpP7U9CcMMZCMIhmZBb0BBF5D7NLWY3a9XAj02EZCaOeksYFpm2bP4rWWthGN2X6MhWuCmokuZAnZAHSa8LYx21FmomqrvoJgtUmO0HhOkTGpqFU0DZA8wy9eKpGwDpxIvim1DhSGbYpK0LSABwZDZD
    #https://graph.facebook.com/me/feed?access_token=CAACZAZApvSluYBAPdgdAF0A2ZCPCnZBOYHHcPmte2ZCuzqkrDZAGLCM1xRQ9eanr8IQBJP09eGFQBHLFN641g1BeJZCj4HZA9xnq3D5i4d0q9OPNXbSjZAiZAaoGVnE54zGAIROMuTSOotXuaFPjK4uZBMXBCZCqy954MGZB7mX91i6bzolsIQG2wzTMdpJeSSKfODwUBTsSJYUV6aypVDyGVLEOedNAYNVUzTHQMCCQLqZCu7QQZDZD

    #Get token from here: https://developers.facebook.com/tools/explorer

    token = 'CAACEdEose0cBAGpZAAjtasaei8JiZCnh6Moob5Bp2YDRwcoxGS9r7v8nV9I5LFl23pLOd443MXyRWEr0vWiynv6IkJ0K3ZBOqe3RI6w7z81ZBlzhRBBrYZAPnrZCYkM0S8gpqXs7rOmyVHuYN548hzocoFAlRodWGxPH3ENqZASlaHAVBgTU7SAc873TTbT9UZAjPN1bi0SeoVKe0CBkuykmzIbtUXM1yqK9cf5L5D63YwZDZD'
    graph = facebook.GraphAPI(token)
    studios = Studio.objects.filter(name_url=studio_url_name)
    studio = studios[0]
    fbUserId = 'balancedyoga' #instructor.fb_userid

    #profile = graph.get_object("me")
    #friends = graph.get_connections("me", "friends")
    #friend_list = [friend['name'] for friend in friends['data']]

    if fbUserId is not None:
        fbFeed = graph.get_connections(fbUserId, "feed")
        feeds = fbFeed['data']
    else:
        feeds = None

    return render_to_response('studio/facebook-feed.html',
                           {'studio': studio,
                            'feeds': feeds, },
                            RequestContext(request))

