from django.template import RequestContext
from django.http import Http404
from django.shortcuts import render_to_response

#from schyoga.models import Instructor
from django.template.response import TemplateResponse, SimpleTemplateResponse
from schyoga.bizobj.page import Page
from schyoga.bizobj.state import State
from schyoga.models import Studio
#from schyoga.models import Event

from schyoga.bizobj.schedule import Schedule

from django.views.generic.base import View, ContextMixin, TemplateResponseMixin
from django.shortcuts import render

import datetime
import facebook

#TODO: Need to provide state_url_name variable in every page so that top-level menus would work properly

class MaximkaResponse(TemplateResponse):
    def get_context_data(self, **kwargs):
        context = super(RandomNumberView, self).get_context_data(**kwargs)
        context['kuku'] = 'bla, bla, bla'
        return context


class Profile( View):

    #template_name='studio/profile.html'
    def get(self, request, state_url_name, studio_url_name):
        # <view logic>

        state = State.createFromUrlName(state_url_name)
        #state = State.createFromUrlName('michigan')

        #person = get_object_or_404(Studio, nameForURL=studio_url_name)


        studios = Studio.objects.filter(nameForURL=studio_url_name)
        studio = studios[0]

        curPage = Page(Page.ENUM_STUDIO_PROFILE)

        # return render(request, 'studio/profile.html', { 'studio': studio,
        #                     'state': state,
        #                      'curPage': curPage})

        # return self.render_to_response({ 'studio': studio,
        #                     'state': state,
        #                      'curPage': curPage} )

        return render_to_response('studio/profile.html',
                          { 'studio': studio,
                            'state': state,
                            'curPage': curPage},
                            RequestContext(request))

    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)
        context['kuku'] = 'bla, bla, bla'
        return context


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


def schedule(request, state_url_name, studio_url_name):

    state = State.createFromUrlName(state_url_name)

    studios = Studio.objects.filter(nameForURL=studio_url_name)
    studio = studios[0]
    eventsTmp = studio.event_set.all().order_by('start_time')

    sched = Schedule(eventsTmp, datetime.datetime(2013, 8, 6), 14)

    curPage = Page(Page.ENUM_STUDIO_SCHEDULE)

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


    token = 'CAACEdEose0cBACiZARJONieRJo4EJbiR9kZAeP299ZBzybETe02ANnfELjyCWuLJwsz2Go2aZCKmdwWah8xnVB0lH2voBIwZANTRGTKmeBU26cRtPpjHUsYDV9ZBU0sPvZCX8xmKv8kuarMZBuU73M3qPnbfUfRkDdYVZALNeFlcGr37beZCRUGsUub4DWfls3aVL9GSNRvpZBdHPnjqni0aklAaH2KltQkV0GL88Dxa15iMQZDZD'
    graph = facebook.GraphAPI(token)
    studios = Studio.objects.filter(nameForURL=studio_url_name)
    studio = studios[0]
    fbUserId = studio.fbPageID  #'balancedyoga' #instructor.fb_userid

    #profile = graph.get_object("me")
    #friends = graph.get_connections("me", "friends")
    #friend_list = [friend['name'] for friend in friends['data']]

    if fbUserId:
        fbFeed = graph.get_connections(fbUserId, "feed")
        feeds = fbFeed['data']
    else:
        feeds = None

    curPage = Page(Page.ENUM_STUDIO_FACEBOOKFEED)

    return render_to_response('studio/facebook-feed.html',
                           {'studio': studio,
                            'state': state,
                            'curPage': curPage,
                            'feeds': feeds, },
                            RequestContext(request))

