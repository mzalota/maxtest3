
from django.template import loader, Context, RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response

from schyoga.models import Instructor
from schyoga.models import Studio
from schyoga.models import Event

from schyoga.bizobj.schedule import Schedule

#import collections
import datetime

import facebook

def schedule(request, state_url_name, teacher_url_name):
    instructors = Instructor.objects.filter(name_url=teacher_url_name)
    instructor = instructors[0]
    events = instructor.event_set.all().order_by('start_time')

    #TODO: filter events from DB by date, so that dates on the calendar correspond with what was pulled from DB

    sched = Schedule(events, datetime.datetime(2013, 8, 5), 14)

    return render_to_response('teacher/schedule.html',
                                {'instructor': instructor,
                                 'calendar': sched,
                                 'num_events': events.count(),},
                                RequestContext(request))


def facebookFeed(request, state_url_name, teacher_url_name):
    #https://www.facebook.com/JeanneEllenHeaton
    #https://graph.facebook.com/JeanneEllenHeaton/feed?access_token=CAAAAAITEghMBAIeRlyE803IvUcjjQ43WPkM44b36XLAnCVZBFjJEF76ZBBXaiDS7kBfSY4fqrEphDiXVZBl9ot9WFGZBCKpP7U9CcMMZCMIhmZBb0BBF5D7NLWY3a9XAj02EZCaOeksYFpm2bP4rWWthGN2X6MhWuCmokuZAnZAHSa8LYx21FmomqrvoJgtUmO0HhOkTGpqFU0DZA8wy9eKpGwDpxIvim1DhSGbYpK0LSABwZDZD
    #https://graph.facebook.com/me/feed?access_token=CAACZAZApvSluYBAPdgdAF0A2ZCPCnZBOYHHcPmte2ZCuzqkrDZAGLCM1xRQ9eanr8IQBJP09eGFQBHLFN641g1BeJZCj4HZA9xnq3D5i4d0q9OPNXbSjZAiZAaoGVnE54zGAIROMuTSOotXuaFPjK4uZBMXBCZCqy954MGZB7mX91i6bzolsIQG2wzTMdpJeSSKfODwUBTsSJYUV6aypVDyGVLEOedNAYNVUzTHQMCCQLqZCu7QQZDZD

    #Get token from here: https://developers.facebook.com/tools/explorer

    token = 'CAACEdEose0cBAFN6ojoBZBPq9vXv9iOJ5WPWHSLQ8jQb4ZC5waEzyYfvUnoMKiTN1Uz6NlWclZCekB2zBahrN2gMZBkUNxCr6VoPOV091AlbeF0HkqmGHMtsbGoUoZAOpmO7ISbFQmDDHRbGiVYgb5QcJpeCtwV5TRebuQaqg7ccwcp0bRkpQQjZB5noudVErpbWypL0pevKYxo0Pk5cAprmLPy8bNypkU35eD2Xx6GQZDZD'
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

    return render_to_response('teacher/facebook-feed.html',
                          { 'instructor': instructor,
                            'feeds': feeds, },
                            RequestContext(request))


def profile(request, state_url_name, teacher_url_name):

    instructors = Instructor.objects.filter(name_url=teacher_url_name)
    instructor = instructors[0]

    return render_to_response('teacher/profile.html',
                          { 'instructor': instructor, },
                            RequestContext(request))


def list(request, state_url_name):
    #list = Instructor.objects.filter(instructor_name="Jeanne Heaton")
    instructors = Instructor.objects.all()

    return render_to_response('teacher/list.html',
                            { 'instructors': instructors,
                              'state_url_name': state_url_name, },
                            context_instance=RequestContext(request))
