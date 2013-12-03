import logging
import datetime
from django.core import serializers
from schyoga.bizobj.parser.scraperOld import ScraperOld
from schyoga.models import Instructor
from schyoga.models.event import Event
from schyoga.models.studio import Studio
from schyoga.scraper.scraper import Scraper
from schyoga.scraper.steps.clickelement import ClickElement
from schyoga.scraper.steps.clicklink import ClickLink
from schyoga.scraper.steps.dealwithnewinstructors import DealWithNewInstructors
from schyoga.scraper.steps.extracteventsfrommbo import ExtractEventsFromMBO
from schyoga.scraper.steps.extracthtmlsnippet import ExtractHtmlSnippet
from schyoga.scraper.steps.linktoknowninstructors import LinkToKnownInstructors
from schyoga.scraper.steps.loadurl import LoadUrl
from schyoga.scraper.steps.prepareeventsfordb import PrepareEventsForDB
from schyoga.scraper.steps.readpagecontent import ReadPageContent
from schyoga.scraper.steps.savehtmltodb import SaveHtmlToDB
from schyoga.scraper.steps.standardizeinstructornames import StandardizeInstructorNames
from schyoga.scraper.steps.waitforelement import WaitForElement
from schyoga.scraper.steps.waitforframe import WaitForFrame

import io, json
import codecs

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
        if step['step_name'] == 'MBOLParseHtml':
            process_step(scraper, studio, step['headers'])
        else:
            logger.error("Unrecognized Parsing step: "+step['step_name'])

    logger.debug("Finished parsing schedule for studio: "+str(studio.id)+", "+studio.name)


    #TODO: Keep track of Assistants. They soon will become teachers (or may be teachig elsewhere). co-Teacher. Assistant2, Acompanist, etc.
    #TODO: validate that headers on the page match configured ones
    #TODO: check that we successfully parsed the page


def process_step(scraper, studio, headers):

    instructors_file_path = "C:/tmp/unknown_instructors2.csv"

    logger.debug("Parsing events out of MindBodyOnline HTML")

    #load from parsing_history
    current_week_num = datetime.datetime.now().isocalendar()[1]
    wk1 = 'week_'+str(current_week_num)
    wk2 = 'week_'+str(current_week_num+1)
    wk3 = 'week_'+str(current_week_num+2)

    htmls = studio.parsing_history_set.filter(comment__in=[wk1, wk2,wk3]) .filter(scrape_uuid__in=["47325061-5b5e-11e3-a69d-00256444d517",'96d274cf-5b6b-11e3-aba8-00256444d517'])
    if not htmls or len(htmls) <= 0:
        logger.error("No parsed_history objects found ")
        return

    #TODO: delete events for this studio from DB

    for html in htmls:
        html_str = html.calendar_html
        db_events = parsing_html(headers, html_str, instructors_file_path, scraper, studio)

        #scraper.vars['db_events'] = db_events

        print_db_events(db_events)
        if db_events:
            for db_event in db_events:
                db_event.save()


def print_db_events(db_events):

    if not db_events:
        logger.debug("No Events were Parsed out:")
        return

    logger.debug("Parsed Out DB Events are :")
    for idx, db_event in enumerate(db_events):
        logger.debug( str(idx)+": "+db_event.comments + ", "+repr(db_event.start_time)+", "+db_event.instructor_name)

    if db_events:
        json_db_events = serializers.serialize('json', db_events)
        print json_db_events


def parsing_html(headers, html_str, instructors_file_path, scraper, studio):

    parsed_events = ExtractEventsFromMBO(scraper).run(html_str, headers)
    db_events = PrepareEventsForDB(scraper).run(studio, parsed_events)
    studio_instructors = studio.instructors.all()
    instructors_unmatched = LinkToKnownInstructors(scraper).run2(studio_instructors, db_events)
    DealWithNewInstructors(scraper).run(studio, instructors_unmatched, instructors_file_path)

    return db_events

