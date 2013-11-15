from operator import attrgetter

from django.template import loader, Context, RequestContext
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from schyoga.bizobj.page import Page

from schyoga.bizobj.schedule import Schedule
from schyoga.bizobj.state import State

from schyoga.models import Instructor
from schyoga.models import Studio
from schyoga.models import Event
from django.views.generic.base import View

#import collections
import datetime
import facebook


def list(request, state_url_name):

    state = State.createFromUrlName(state_url_name)
    if state is None:
        raise Http404

    #list = Instructor.objects.filter(instructor_name="Jeanne Heaton")
    instructors = Instructor.objects.all().filter(state_name_url=state_url_name).order_by('instructor_name')

    #instructors = sorted(instructors, key=attrgetter('instructor_name'))


    return render_to_response('teacher/list.html',
                            { 'instructors': instructors,
                              'state': state, },
                            context_instance=RequestContext(request))


class TeacherViews(View):
    pagename = ''

    def get(self, request, state_url_name, teacher_url_name):

        curPage = Page.createFromEnum(self.pagename)
        if not curPage:
            assert "Invalid parameter to instantiate Page object"

        instructor = get_object_or_404(Instructor, name_url=teacher_url_name)

        state = State.createFromUrlName(state_url_name)
        if not state:
            newURL = curPage.urlForTeacherPage(instructor)
            response = HttpResponse(content="", status=301)
            response["Location"] = newURL
            return response

        if self.pagename == Page.ENUM_TEACHER_PROFILE:
            return self.profile(request, instructor, state, curPage)
        if self.pagename == Page.ENUM_TEACHER_SCHEDULE:
            return self.schedule(request, instructor, state, curPage)
        if self.pagename == Page.ENUM_TEACHER_FACEBOOKFEED:
            return self.facebook_feed(request, instructor, state, curPage)


    def profile(self, request, instructor, state, cur_page):

        startDateStr = datetime.datetime.now().strftime('%Y-%m-%d')
        events = instructor.event_set.all().order_by('start_time').filter(start_time__gt=startDateStr)
        calendar = Schedule(events)

        return render_to_response('teacher/profile.html',
                                  {'instructor': instructor,
                                   'state': state,
                                   'curPage': cur_page,
                                   'calendar': calendar},
                                  RequestContext(request))

    def schedule(self, request, instructor, state, cur_page):
        #TODO: V.2. filter events from DB by date, so that dates on the calendar correspond with what was pulled from DB

        startDate = datetime.datetime.now()
        startDateStr = startDate.strftime('%Y-%m-%d')
        events = instructor.event_set.all().order_by('start_time').filter(start_time__gt=startDateStr)

        calendar = Schedule(events, startDate)
        #sched = Schedule(events, datetime.datetime(2013, 8, 6), 14)

        return render_to_response('teacher/schedule.html',
                                  {'instructor': instructor,
                                   'state': state,
                                   'curPage': cur_page,
                                   'calendar': calendar},
                                  RequestContext(request))

    def facebook_feed(self, request, instructor, state, curPage):

        #TODO: V.2. make Facebook Page look prettier before rolling it out

        #https://www.facebook.com/JeanneEllenHeaton
        #https://graph.facebook.com/JeanneEllenHeaton/feed?access_token=CAAAAAITEghMBAIeRlyE803IvUcjjQ43WPkM44b36XLAnCVZBFjJEF76ZBBXaiDS7kBfSY4fqrEphDiXVZBl9ot9WFGZBCKpP7U9CcMMZCMIhmZBb0BBF5D7NLWY3a9XAj02EZCaOeksYFpm2bP4rWWthGN2X6MhWuCmokuZAnZAHSa8LYx21FmomqrvoJgtUmO0HhOkTGpqFU0DZA8wy9eKpGwDpxIvim1DhSGbYpK0LSABwZDZD
        #https://graph.facebook.com/me/feed?access_token=CAACZAZApvSluYBAPdgdAF0A2ZCPCnZBOYHHcPmte2ZCuzqkrDZAGLCM1xRQ9eanr8IQBJP09eGFQBHLFN641g1BeJZCj4HZA9xnq3D5i4d0q9OPNXbSjZAiZAaoGVnE54zGAIROMuTSOotXuaFPjK4uZBMXBCZCqy954MGZB7mX91i6bzolsIQG2wzTMdpJeSSKfODwUBTsSJYUV6aypVDyGVLEOedNAYNVUzTHQMCCQLqZCu7QQZDZD

        #Get token from here: https://developers.facebook.com/tools/explorer
        token = 'CAACEdEose0cBAJfVdqZCjPr0luXW6G6WCmRcL9zTaCMbwCYeQUIh4X480NWakFa4VyTdUNPauKyUOJcGbuHRTxbxYm7Ik3tOR6pZCsVipmy5K32ZBSBiCZByIOvNK2a4ZCzdh7hMNOE0fQvFmh7tY4swtbZCmHrg9yUDRZASOGDcd3CHORfkxEZBQrG2yZBc5VRJtE3Q8BUzO3Wj6hNRVT13N7v7bvNHeXMlgj3nZALDdn9wZDZD'
        graph = facebook.GraphAPI(token)

        fbUserId = instructor.fb_id

        #profile = graph.get_object("me")
        #friends = graph.get_connections("me", "friends")
        #friend_list = [friend['name'] for friend in friends['data']]

        if fbUserId:
            fbFeed = graph.get_connections(fbUserId, "feed")
            feeds = fbFeed['data']
        else:
            feeds = None

        return render_to_response('teacher/facebook-feed.html',
                                  {'instructor': instructor,
                                   'state': state,
                                   'curPage': curPage,
                                   'feeds': feeds, },
                                  RequestContext(request))
