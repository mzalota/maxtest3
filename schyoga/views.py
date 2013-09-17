# Create your views here.

from django.template import loader, Context, RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response

from schyoga.models import Instructor
from schyoga.models import Studio
from schyoga.models import Event


import collections
import datetime
#from django_facebook.middleware import FacebookMiddleware
import facebook


def siteMap(request):
    return render_to_response('site-map.html', {}, RequestContext(request))


def shoutOuts(request):
    return render_to_response('shout-outs.html', {}, RequestContext(request))


def instructorSchedule(request, instructor_url_name):
    instructors = Instructor.objects.filter(name_url=instructor_url_name)
    instructor = instructors[0]
    events = instructor.event_set.all().order_by('start_time')


    #startTimes dictionary - key is event start_time and value is array of events that start at that time.
    startTimes = collections.OrderedDict()
    for event in events:
        startTimeStr = event.start_time.strftime('%H:%M')
        dayOfWeek = event.start_time.strftime('%x')
        if not startTimeStr in startTimes:
            startTimes[startTimeStr] = collections.OrderedDict() # dict() #first time that a key is inserted to the dictionary initalize value to be a list

        if not dayOfWeek in startTimes[startTimeStr]:
            startTimes[startTimeStr][dayOfWeek] = list() #first time that a key is inserted to the dictionary initalize value to be a list

        startTimes[startTimeStr][dayOfWeek].append(event)


    calendarDates = [datetime.datetime(2013, 8, 5).strftime('%x'),
                     datetime.datetime(2013, 8, 6).strftime('%x'),
                     datetime.datetime(2013, 8, 7).strftime('%x'),
                     datetime.datetime(2013, 8, 8).strftime('%x'),
                     datetime.datetime(2013, 8, 9).strftime('%x'),
                     datetime.datetime(2013, 8, 10).strftime('%x'),
                     datetime.datetime(2013, 8, 11).strftime('%x'),
                     datetime.datetime(2013, 8, 12).strftime('%x'),
                     datetime.datetime(2013, 8, 13).strftime('%x'),
                     datetime.datetime(2013, 8, 14).strftime('%x'),
                     datetime.datetime(2013, 8, 15).strftime('%x'),
                     datetime.datetime(2013, 8, 16).strftime('%x'),
                     datetime.datetime(2013, 8, 17).strftime('%x'),
                     datetime.datetime(2013, 8, 18).strftime('%x'),
                     datetime.datetime(2013, 8, 19).strftime('%x'),]

    return render_to_response('instructor-schedule.html',
                              {'instructor': instructor, 'events': events, 'startTimes': startTimes , 'calendarDates': calendarDates, },
                              RequestContext(request))


def instructorFacebookFeed(request, instructor_url_name):
    #https://www.facebook.com/JeanneEllenHeaton
    #https://graph.facebook.com/JeanneEllenHeaton/feed?access_token=CAAAAAITEghMBAIeRlyE803IvUcjjQ43WPkM44b36XLAnCVZBFjJEF76ZBBXaiDS7kBfSY4fqrEphDiXVZBl9ot9WFGZBCKpP7U9CcMMZCMIhmZBb0BBF5D7NLWY3a9XAj02EZCaOeksYFpm2bP4rWWthGN2X6MhWuCmokuZAnZAHSa8LYx21FmomqrvoJgtUmO0HhOkTGpqFU0DZA8wy9eKpGwDpxIvim1DhSGbYpK0LSABwZDZD
    #https://graph.facebook.com/me/feed?access_token=CAACZAZApvSluYBAPdgdAF0A2ZCPCnZBOYHHcPmte2ZCuzqkrDZAGLCM1xRQ9eanr8IQBJP09eGFQBHLFN641g1BeJZCj4HZA9xnq3D5i4d0q9OPNXbSjZAiZAaoGVnE54zGAIROMuTSOotXuaFPjK4uZBMXBCZCqy954MGZB7mX91i6bzolsIQG2wzTMdpJeSSKfODwUBTsSJYUV6aypVDyGVLEOedNAYNVUzTHQMCCQLqZCu7QQZDZD

    #Get token from here: https://developers.facebook.com/tools/explorer

    token = 'CAACEdEose0cBAFN6ojoBZBPq9vXv9iOJ5WPWHSLQ8jQb4ZC5waEzyYfvUnoMKiTN1Uz6NlWclZCekB2zBahrN2gMZBkUNxCr6VoPOV091AlbeF0HkqmGHMtsbGoUoZAOpmO7ISbFQmDDHRbGiVYgb5QcJpeCtwV5TRebuQaqg7ccwcp0bRkpQQjZB5noudVErpbWypL0pevKYxo0Pk5cAprmLPy8bNypkU35eD2Xx6GQZDZD'
    graph = facebook.GraphAPI(token)
    instructors = Instructor.objects.filter(name_url=instructor_url_name)
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

    return render_to_response('instructor-facebook-feed.html',
                          { 'instructor': instructor, 'feeds': feeds, },
                            RequestContext(request))


def instructor(request, instructor_url_name):

    instructors = Instructor.objects.filter(name_url=instructor_url_name)
    instructor = instructors[0]



    return render_to_response('instructor.html',
                          { 'instructor': instructor,},
                            RequestContext(request))


def instructors(request):
    #instructors = Instructor.objects.filter(instructor_name="Jeanne Heaton")
    instructors = Instructor.objects.all()

    return render_to_response('instructors.html',
                            { 'instructors': instructors, },
                            context_instance=RequestContext(request))


def studios(request):
    studios = Studio.objects.all()
    #t = loader.get_template("studios.html")
    #c = Context({'studios': studios})
    #return HttpResponse(t.render(c))
    return render_to_response('studios.html',
                            { 'studios': studios, },
                            context_instance=RequestContext(request))


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