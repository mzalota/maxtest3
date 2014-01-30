import logging

import logging
import datetime
from schyoga.bizobj.schedule import Schedule

from schyoga.scraper.steps.dealwithnewinstructors import DealWithNewInstructors
from schyoga.scraper.steps.extracteventsfrommbo import ExtractEventsFromMBO
from schyoga.scraper.steps.filterevents import FilterEvents

from schyoga.scraper.steps.linktoknowninstructors import LinkToKnownInstructors

from schyoga.scraper.steps.prepareeventsfordb import PrepareEventsForDB


logger = logging.getLogger(__name__)


class parseMBO:
    def __init__(self, scraper):
        self.scraper = scraper


    def run(self, studio, headers, filters):
        logger.debug("Parsing MBO: ")

        #self.scraper.browser.find_element_by_partial_link_text(link_text).click()
        events = self.process_step(studio, headers, filters)

        logger.debug("Finished Parsing MBO: ")
        return events

    def retrieve_html_by_week(self, studio, week_num, year):
        """

        @type studio: Studio
        @type week_num: Int
        @type year: Int
        @rtype: str
        """

        week_str = "{0:0>2}".format(week_num)
        comment = 'week_' + str(year) + '_' + week_str

        logger.debug("fetching parsing history for: " + comment)
        #htmls = studio.parsing_history_set.filter(comment__in=[wk1, wk2,wk3]).order_by('-last_crawling')[0] #.filter(scrape_uuid__in=['c524960f-81e5-11e3-a0ec-00256444d517','7ac9da6e-81f0-11e3-a553-00256444d517','f6c613b0-81ef-11e3-8215-00256444d517'])

        try:
            parsing_history = studio.parsing_history_set.filter(comment__in=[comment]).order_by('-last_crawling')[0]
                #.filter(scrape_uuid__in=['c524960f-81e5-11e3-a0ec-00256444d517','7ac9da6e-81f0-11e3-a553-00256444d517','f6c613b0-81ef-11e3-8215-00256444d517'])
        except IndexError:
            logger.error("Did not find parsing history for: "+ comment+' for studio: '+studio.name)
            return None

        return parsing_history.calendar_html


    def retrieve_htmls_by_date(self, studio, date, num_of_weeks):
        htmls = list()
        #for offset in [0, 1, 2]:
        for offset in list(range(0, num_of_weeks)):
            target_date = date + datetime.timedelta(weeks=offset)
            target_date_iso = target_date.isocalendar()
            target_week_num = target_date_iso[1]
            target_year = target_date_iso[0]
            html = self.retrieve_html_by_week(studio, target_week_num, target_year)
            if html:
                htmls.append(html)
        return htmls

    def process_step(self, studio, headers, filters):
        """

        @type studio: Studio
        @param headers:
        @param filters:
        @rtype: list of Event
        """
        instructors_file_path = "C:/tmp/unknown_instructors3.csv"

        logger.debug("Parsing events out of MindBodyOnline HTML")

        #load from parsing_history
        today = datetime.datetime.now()
        htmls = self.retrieve_htmls_by_date(studio, today, 3)

        if not htmls or len(htmls) <= 0:
            logger.error("No parsed_history objects found ")
            return

        #delete events for this studio from DB
        start_time, end_time = Schedule.get_week_start_and_end_for_date(today)
        start_time_str = start_time.strftime('%Y-%m-%d')
        end_time_str = end_time.strftime('%Y-%m-%d')
        logger.debug("deleting events for studio: "+studio.name+"between date range: "+start_time_str+" and "+end_time_str)
        studio.event_set.filter(start_time__gte=start_time_str).delete() #.filter(start_time__lt=end_time_str)

        all_events = list()
        for html_str in htmls:
            #html_str = html.calendar_html
            db_events = self.parsing_html(headers, html_str, instructors_file_path, studio, filters)

            #scraper.vars['db_events'] = db_events
            #print_db_events(db_events)

            if db_events:
                #logger.info("Saving " + str(len(db_events)) + " events to DB")
                #for db_event in db_events:
                #    db_event.save()
                #    pass
                all_events = all_events + db_events

        return all_events


    def parsing_html(self, headers, html_str, instructors_file_path, studio, filters):
        """

        @param headers:
        @param html_str:
        @param instructors_file_path:
        @param studio:
        @param filters:
        @rtype: list of Event
        """
        parsed_events = ExtractEventsFromMBO(self.scraper).run(html_str, headers)
        parsed_events_new = FilterEvents(self.scraper).run(parsed_events, filters)
        db_events = PrepareEventsForDB(self.scraper).run(studio, parsed_events_new)
        studio_instructors = studio.instructors.all()
        instructors_unmatched = LinkToKnownInstructors(self.scraper).run2(studio_instructors, db_events)
        DealWithNewInstructors(self.scraper).run(studio, instructors_unmatched, instructors_file_path)

        return db_events

