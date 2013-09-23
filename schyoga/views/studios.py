from django.template import loader, Context, RequestContext
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response

#from schyoga.models import Instructor
from schyoga.bizobj.state import State
from schyoga.models import Studio
#from schyoga.models import Event

from schyoga.bizobj.schedule import Schedule

import datetime
import facebook

#TODO: Need to provide state_url_name variable in every page so that top-level menus would work properly


class StudioPage:
    ENUM_STUDIO_PROFILE = 1
    ENUM_STUDIO_SCHEDULE = 2
    ENUM_STUDIO_FACEBOOKFEED = 3

    def __init__(self, curPageID):
        self.id = curPageID



def list(request, state_url_name):

    state = State.createFromUrlName(state_url_name)
    if state is None:
        raise Http404

    studios = Studio.objects.all().filter(state_name_url=state_url_name).order_by('name')
    #t = loader.get_template("list.html")
    #c = Context({'studios': studios})
    #return HttpResponse(t.render(c))


    return render_to_response('studio/list.html',
                            { 'studios': studios,
                              'state': state, },
                            context_instance=RequestContext(request))

def profile(request, state_url_name, studio_url_name):

    state = State.createFromUrlName(state_url_name)

    #person = get_object_or_404(Studio, nameForURL=studio_url_name)

    studios = Studio.objects.filter(nameForURL=studio_url_name)
    studio = studios[0]

    curPage = StudioPage(StudioPage.ENUM_STUDIO_PROFILE)

    return render_to_response('studio/profile.html',
                          { 'studio': studio,
                            'state': state,
                            'curPage': curPage},
                            RequestContext(request))


def schedule(request, state_url_name, studio_url_name):

    state = State.createFromUrlName(state_url_name)

    studios = Studio.objects.filter(nameForURL=studio_url_name)
    studio = studios[0]
    eventsTmp = studio.event_set.all().order_by('start_time')

    sched = Schedule(eventsTmp, datetime.datetime(2013, 8, 6), 14)

    curPage = StudioPage(StudioPage.ENUM_STUDIO_SCHEDULE)

    return render_to_response('studio/schedule.html',
                                {'studio': studio,
                                 'state': state,
                                 'curPage': curPage,
                                 'calendar': sched, },
                              RequestContext(request))

def facebookFeed(request, state_url_name, studio_url_name):
    #https://www.facebook.com/JeanneEllenHeaton
    #https://graph.facebook.com/JeanneEllenHeaton/feed?access_token=CAAAAAITEghMBAIeRlyE803IvUcjjQ43WPkM44b36XLAnCVZBFjJEF76ZBBXaiDS7kBfSY4fqrEphDiXVZBl9ot9WFGZBCKpP7U9CcMMZCMIhmZBb0BBF5D7NLWY3a9XAj02EZCaOeksYFpm2bP4rWWthGN2X6MhWuCmokuZAnZAHSa8LYx21FmomqrvoJgtUmO0HhOkTGpqFU0DZA8wy9eKpGwDpxIvim1DhSGbYpK0LSABwZDZD
    #https://graph.facebook.com/me/feed?access_token=CAACZAZApvSluYBAPdgdAF0A2ZCPCnZBOYHHcPmte2ZCuzqkrDZAGLCM1xRQ9eanr8IQBJP09eGFQBHLFN641g1BeJZCj4HZA9xnq3D5i4d0q9OPNXbSjZAiZAaoGVnE54zGAIROMuTSOotXuaFPjK4uZBMXBCZCqy954MGZB7mX91i6bzolsIQG2wzTMdpJeSSKfODwUBTsSJYUV6aypVDyGVLEOedNAYNVUzTHQMCCQLqZCu7QQZDZD

    #Get token from here: https://developers.facebook.com/tools/explorer

    state = State.createFromUrlName(state_url_name)


    token = 'CAACEdEose0cBAAZBO48lL1H0fcHRBVZA97YVpM3q11MOb7xPBUhJTmZAXeyFYaqNU4ZAXz34Mw51EaNoCsak1hvczyxVgGz8A7JsmZCf4drZADmZB3w3gQRoQur3mTdqMHOwBc5eAiwYogSVLvqZCJIRkTYPbbh5o7PCKPQxhTRxli7E93JLtNH2UMftJkv8huq9Q4JvoHk7ERZBzgBbwSgYtBpn2SanAKVyBTjNZAdwN7vwZDZD'
    graph = facebook.GraphAPI(token)
    studios = Studio.objects.filter(nameForURL=studio_url_name)
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

    curPage = StudioPage(StudioPage.ENUM_STUDIO_FACEBOOKFEED)

    return render_to_response('studio/facebook-feed.html',
                           {'studio': studio,
                            'state': state,
                            'curPage': curPage,
                            'feeds': feeds, },
                            RequestContext(request))

