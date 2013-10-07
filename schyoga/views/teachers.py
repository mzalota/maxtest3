from operator import attrgetter

from django.template import loader, Context, RequestContext
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from schyoga.bizobj.page import Page

from schyoga.bizobj.schedule import Schedule
from schyoga.bizobj.state import State

from schyoga.models import Instructor
from schyoga.models import Studio
from schyoga.models import Event

#import collections
import datetime

import facebook


def list(request, state_url_name):

    state = State.createFromUrlName(state_url_name)
    if state is None:
        raise Http404

    #list = Instructor.objects.filter(instructor_name="Jeanne Heaton")
    instructors = Instructor.objects.all().order_by('instructor_name')

    #instructors = sorted(instructors, key=attrgetter('instructor_name'))



    return render_to_response('teacher/list.html',
                            { 'instructors': instructors,
                              'state': state, },
                            context_instance=RequestContext(request))



def profile(request, state_url_name, teacher_url_name):

    state = State.createFromUrlName(state_url_name)

    instructors = Instructor.objects.filter(name_url=teacher_url_name)
    instructor = instructors[0]
    events = instructor.event_set.all().order_by('start_time')
    sched = Schedule(events)

    curPage = Page(Page.ENUM_TEACHER_PROFILE)

    return render_to_response('teacher/profile.html',
                          { 'instructor': instructor,
                            'state': state,
                            'curPage': curPage,
                            'calendar': sched,},
                            RequestContext(request))



def schedule(request, state_url_name, teacher_url_name):

    startDate = datetime.datetime.now()
    startDateStr = startDate.strftime('%Y-%m-%d')

    state = State.createFromUrlName(state_url_name)

    instructors = Instructor.objects.filter(name_url=teacher_url_name)
    instructor = instructors[0]
    events = instructor.event_set.all().order_by('start_time').filter(start_time__gt=startDateStr)

    #TODO: filter events from DB by date, so that dates on the calendar correspond with what was pulled from DB

    #sched = Schedule(events, datetime.datetime(2013, 8, 5), 14)
    sched = Schedule(events, startDate)

    curPage = Page(Page.ENUM_TEACHER_SCHEDULE)

    return render_to_response('teacher/schedule.html',
                                {'instructor': instructor,
                                 'state': state,
                                 'curPage': curPage,
                                 'calendar': sched,
                                 'num_events': events.count(),},
                                RequestContext(request))


def facebookFeed(request, state_url_name, teacher_url_name):

    state = State.createFromUrlName(state_url_name)

    #https://www.facebook.com/JeanneEllenHeaton
    #https://graph.facebook.com/JeanneEllenHeaton/feed?access_token=CAAAAAITEghMBAIeRlyE803IvUcjjQ43WPkM44b36XLAnCVZBFjJEF76ZBBXaiDS7kBfSY4fqrEphDiXVZBl9ot9WFGZBCKpP7U9CcMMZCMIhmZBb0BBF5D7NLWY3a9XAj02EZCaOeksYFpm2bP4rWWthGN2X6MhWuCmokuZAnZAHSa8LYx21FmomqrvoJgtUmO0HhOkTGpqFU0DZA8wy9eKpGwDpxIvim1DhSGbYpK0LSABwZDZD
    #https://graph.facebook.com/me/feed?access_token=CAACZAZApvSluYBAPdgdAF0A2ZCPCnZBOYHHcPmte2ZCuzqkrDZAGLCM1xRQ9eanr8IQBJP09eGFQBHLFN641g1BeJZCj4HZA9xnq3D5i4d0q9OPNXbSjZAiZAaoGVnE54zGAIROMuTSOotXuaFPjK4uZBMXBCZCqy954MGZB7mX91i6bzolsIQG2wzTMdpJeSSKfODwUBTsSJYUV6aypVDyGVLEOedNAYNVUzTHQMCCQLqZCu7QQZDZD

    #Get token from here: https://developers.facebook.com/tools/explorer

    token = 'CAACEdEose0cBACiZARJONieRJo4EJbiR9kZAeP299ZBzybETe02ANnfELjyCWuLJwsz2Go2aZCKmdwWah8xnVB0lH2voBIwZANTRGTKmeBU26cRtPpjHUsYDV9ZBU0sPvZCX8xmKv8kuarMZBuU73M3qPnbfUfRkDdYVZALNeFlcGr37beZCRUGsUub4DWfls3aVL9GSNRvpZBdHPnjqni0aklAaH2KltQkV0GL88Dxa15iMQZDZD'
    graph = facebook.GraphAPI(token)
    instructors = Instructor.objects.filter(name_url=teacher_url_name)
    instructor = instructors[0]
    fbUserId = instructor.fb_userid

    #profile = graph.get_object("me")
    #friends = graph.get_connections("me", "friends")
    #friend_list = [friend['name'] for friend in friends['data']]

    if fbUserId is not None:
        fbFeed = graph.get_connections(fbUserId, "feed")
        feeds = fbFeed['data']
    else:
        feeds = None

    curPage = Page(Page.ENUM_TEACHER_FACEBOOKFEED)

    return render_to_response('teacher/facebook-feed.html',
                          { 'instructor': instructor,
                            'state': state,
                            'curPage': curPage,
                            'feeds': feeds, },
                            RequestContext(request))
