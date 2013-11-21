#from schyoga.models import Event

import collections
import datetime

from operator import itemgetter, attrgetter
#from schyoga.models import Event
import schyoga.models.event

class Schedule():

    def __init__(self, events, startDate=datetime.datetime.now(), numDays=14):
        self.events = events
        self.__startDate = startDate
        self.__numDays = numDays

        self.__orgEvents = self.__initOrganizedEvents(events)

        self.calendarTimesStr = self.__initStartTimes(events)

        self.calendarDates, self.calendarDatesStr = self.__initCalendarDates(startDate, numDays)

    def __initCalendarDates(self, startDate, numDays):
        calendarDates = []
        calendarDatesStr = []
        for i in range(numDays):
            curDate = startDate + datetime.timedelta(days=i)
            calendarDates.append(curDate)
            calendarDatesStr.append(curDate.strftime('%x'))

        return calendarDates, calendarDatesStr

    def __initStartTimes(self, events):
        startTimesStr = []
        distinctDates = []
        for event in self.events:
            startTimeStr = event.start_time.strftime('%H:%M')
            if not startTimeStr in startTimesStr:
                startTimesStr.append(startTimeStr)

        startTimesStr.sort()
        return startTimesStr


    def __initOrganizedEvents(self, events):
        """
        returns  dictionary - key is event start_time and value is array of events that start at that time.

        :return: collections.OrderedDict
        """
        startTimes = collections.OrderedDict()
        for event in events:
            startTimeStr = event.start_time.strftime('%H:%M')
            dayOfWeek = event.start_time.strftime('%x')
            if not startTimeStr in startTimes:
                startTimes[startTimeStr] = collections.OrderedDict() # dict() #first time that a key is inserted to the dictionary initalize value to be a list

            if not dayOfWeek in startTimes[startTimeStr]:
                startTimes[startTimeStr][dayOfWeek] = list() #first time that a key is inserted to the dictionary initalize value to be a list

            startTimes[startTimeStr][dayOfWeek].append(event)

        return startTimes

    def getNumOfEvents(self):
        return self.events.count()

    def getDistinctStudios(self):
        studios = set()
        for event in self.events:
            studios.add(event.studio)

        sortedStudios = sorted(studios, key=attrgetter('name'))
        return sortedStudios


    def getDistinctInstructors(self):
        instructors = set()
        for event in self.events:
            if event.instructor:
                instructors.add(event.instructor)

        sortedInstructors = sorted(instructors, key=attrgetter('instructor_name'))
        return sortedInstructors


    def getEventsByDateAndTime(self, eventDate, eventTimeStr):
        eventDate = eventDate.strftime('%x')

        if not eventTimeStr in self.__orgEvents:
            return None;

        if not eventDate in self.__orgEvents[eventTimeStr]:
            return None

        return self.__orgEvents[eventTimeStr][eventDate]