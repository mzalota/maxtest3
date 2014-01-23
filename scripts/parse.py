import logging
import datetime
import time
from schyoga.bizobj.parser.scraperOld import ScraperOld

from schyoga.models.event import Event
from schyoga.models.studio import Studio
from schyoga.scraper.scraper import Scraper

from schyoga.scraper.steps.dealwithnewinstructors import DealWithNewInstructors
from schyoga.scraper.steps.extracteventsfrommbo import ExtractEventsFromMBO
from schyoga.scraper.steps.filterevents import FilterEvents

from schyoga.scraper.steps.linktoknowninstructors import LinkToKnownInstructors

from schyoga.scraper.steps.prepareeventsfordb import PrepareEventsForDB

import json


logger = logging.getLogger(__name__)


#TODO: V.2. deal with YogaNesh schedule - it has extra rows with "Yoga" or "Dance" heading in the first column
#TODO V.2. deal with case when  there is "no scheduled classes or training sessions" messaage in calendar e.g. for "Yoga Union Center For Backcare & Scoliosis"

def run():

    logger.debug("starting script: parse")

    scraper = Scraper()
    studios = Studio.objects.all().filter(id__gte=1).filter(id__lte=200).order_by('id')
    for studio in studios:
        process_studio(scraper, studio)

    logger.debug('At the end of script: parse')


def process_studio(scraper, studio):
    """

    @type scraper: Scraper
    @type studio: Studio
    """
    logger.debug("Starting to Parse schedule for studio: "+str(studio.id)+", "+studio.name)

    studio_site_set = studio.studio_site_set.all()
    if not studio_site_set:
        logger.error("Config data is not specified for studio: "+str(studio.id)+", "+studio.name)
        return

    if len(studio_site_set)>1:
        logger.error("More then one Studio_Site object exists for  studio: "+str(studio.id)+", "+studio.name)
        return

    config_parse_json = studio_site_set[0].config_parse
    if not config_parse_json or (len(config_parse_json)) <=0:
        logger.error("No Parse Config found! Skipping studio: "+str(studio.id)+", "+studio.name)
        return

    config_parse = json.loads(config_parse_json)



    for step in config_parse:
        logger.debug("Processing step: "+step['step_name'])
        if (step.has_key('filters')):
            filters = step['filters']
        else:
            filters = None
        if step['step_name'] == 'MBOLParseHtml':
            process_step(scraper, studio, step['headers'],filters)
        else:
            logger.error("Unrecognized Parsing step: "+step['step_name'])

    logger.debug("Finished parsing schedule for studio: "+str(studio.id)+", "+studio.name)


    #TODO: Keep track of Assistants. They soon will become teachers (or may be teachig elsewhere). co-Teacher. Assistant2, Acompanist, etc.
    #TODO: validate that headers on the page match configured ones
    #TODO: check that we successfully parsed the page



#this snippet came from here
#http://stackoverflow.com/questions/304256/whats-the-best-way-to-find-the-inverse-of-datetime-isocalendar
def iso_year_start(iso_year):
    "The gregorian calendar date of the first day of the given ISO year"
    fourth_jan = datetime.date(iso_year, 1, 4)
    delta = datetime.timedelta(fourth_jan.isoweekday()-1)
    return fourth_jan - delta

def iso_to_gregorian(iso_year, iso_week, iso_day):
    "Gregorian calendar date for the given ISO year, week and day"
    year_start = iso_year_start(iso_year)
    return year_start + datetime.timedelta(days=iso_day-1, weeks=iso_week-1)


def process_step(scraper, studio, headers, filters):

    instructors_file_path = "C:/tmp/unknown_instructors3.csv"

    logger.debug("Parsing events out of MindBodyOnline HTML")

    #load from parsing_history
    current_date_iso = datetime.datetime.now().isocalendar()
    current_week_num = current_date_iso[1]
    current_year = current_date_iso[0]
    wk1 = 'week_'+str(current_week_num)
    wk2 = 'week_'+str(current_week_num+1)
    wk3 = 'week_'+str(current_week_num+2)

    htmls = studio.parsing_history_set.filter(comment__in=[wk1, wk2,wk3]) .filter(scrape_uuid__in=['c524960f-81e5-11e3-a0ec-00256444d517','7ac9da6e-81f0-11e3-a553-00256444d517','f6c613b0-81ef-11e3-8215-00256444d517'])
    if not htmls or len(htmls) <= 0:
        logger.error("No parsed_history objects found ")
        return

    #delete events for this studio from DB
    first_day_of_the_week_iso=(current_date_iso[0],current_date_iso[1],1)
    first_day_of_the_week_gregorian = iso_to_gregorian(*first_day_of_the_week_iso)
    date_str = str(first_day_of_the_week_gregorian.year)+"-"+str(first_day_of_the_week_gregorian.month)+"-"+str(first_day_of_the_week_gregorian.day)+" 00:00:00"
    studio.event_set.filter(start_time__gte=date_str).delete()

    for html in htmls:
        html_str = html.calendar_html
        db_events = parsing_html(headers, html_str, instructors_file_path, scraper, studio, filters)

        #scraper.vars['db_events'] = db_events
        #print_db_events(db_events)

        if db_events:
            logger.info("Saving to DB "+str(len(db_events))+" to DB")
            for db_event in db_events:
                db_event.save()


def parsing_html(headers, html_str, instructors_file_path, scraper, studio, filters):

    parsed_events = ExtractEventsFromMBO(scraper).run(html_str, headers)

    parsed_events_new = FilterEvents(scraper).run(parsed_events,filters)

    db_events = PrepareEventsForDB(scraper).run(studio, parsed_events_new)
    studio_instructors = studio.instructors.all()
    instructors_unmatched = LinkToKnownInstructors(scraper).run2(studio_instructors, db_events)
    DealWithNewInstructors(scraper).run(studio, instructors_unmatched, instructors_file_path)

    return db_events

