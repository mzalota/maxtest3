#from schyoga.models import Event

import collections
import datetime
import logging
from django.core import serializers

from operator import itemgetter, attrgetter
#from schyoga.models import Event
#import schyoga.models.event

logger = logging.getLogger(__name__)

class Schedule():

    def __init__(self, events, startDate, numDays=14):
        if not startDate:
            startDate=datetime.datetime.now()

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


    def print_db_events(self):
        if not self.events:
            logger.debug("No Events to print:")
            return

        logger.debug("Events are:")
        for idx, event in enumerate(self.events):
            logger.debug( str(idx)+": "+event.comments + ", "+repr(event.start_time)+", "+event.instructor_name)

        if self.events:
            json_db_events = serializers.serialize('json', self.events)
            logger.debug( json_db_events)





    @staticmethod
    def get_week_start_and_end_for_date(date):
        """
        Return the date of Monday before and after parameter

        @type date: datetime.datetime
        @rtype: datetime.datetime
        @rtype: datetime.datetime
        """

        current_date_iso = date.isocalendar()
        current_week_num = current_date_iso[1]
        current_year = current_date_iso[0]
        first_day_of_the_week_iso = (current_year, current_week_num, 1)
        first_day_of_the_week_gregorian = Schedule.iso_to_gregorian(*first_day_of_the_week_iso)

        start_date = datetime.datetime(first_day_of_the_week_gregorian.year, first_day_of_the_week_gregorian.month,first_day_of_the_week_gregorian.day)
        end_date = start_date + datetime.timedelta(days=7)

        return start_date, end_date

    #@staticmethod
    #def get_week_start_and_end_for_week(year, week_num):
    #    first_day_of_the_week_iso = (year, week_num, 1)
    #    first_day_of_the_week_gregorian = Schedule.iso_to_gregorian(*first_day_of_the_week_iso)
    #
    #    start_date = datetime.datetime(first_day_of_the_week_gregorian.year, first_day_of_the_week_gregorian.month,first_day_of_the_week_gregorian.day)
    #    end_date = start_date + datetime.timedelta(days=7)
    #
    #    return start_date, end_date
    #
    #this snippet came from here
    #http://stackoverflow.com/questions/304256/whats-the-best-way-to-find-the-inverse-of-datetime-isocalendar
    @staticmethod
    def iso_year_start(iso_year):
        "The gregorian calendar date of the first day of the given ISO year"
        fourth_jan = datetime.date(iso_year, 1, 4)
        delta = datetime.timedelta(fourth_jan.isoweekday() - 1)
        return fourth_jan - delta

    @staticmethod
    def iso_to_gregorian(iso_year, iso_week, iso_day):
        "Gregorian calendar date for the given ISO year, week and day"
        year_start = Schedule.iso_year_start(iso_year)
        return year_start + datetime.timedelta(days=iso_day - 1, weeks=iso_week - 1)
