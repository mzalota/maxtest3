import logging
from schyoga.bizobj.parser.scraperOld import ScraperOld
from schyoga.models import Event
from schyoga.scraper.scraper import Scraper
from schyoga.scraper.steps.clickelement import ClickElement
from schyoga.scraper.steps.clicklink import ClickLink
from schyoga.scraper.steps.extracteventsfrommbo import ExtractEventsFromMBO
from schyoga.scraper.steps.extracthtmlsnippet import ExtractHtmlSnippet
from schyoga.scraper.steps.linktoknowninstructors import LinkToKnownInstructors
from schyoga.scraper.steps.loadurl import LoadUrl
from schyoga.scraper.steps.prepareeventsfordb import PrepareEventsForDB
from schyoga.scraper.steps.readpagecontent import ReadPageContent
from schyoga.scraper.steps.waitforelement import WaitForElement
from schyoga.scraper.steps.waitforframe import WaitForFrame

from schyoga.models import Studio

logger = logging.getLogger(__name__)

def run():

    logger.debug("starting script: refresh")

    scraper = Scraper()
    url = "https://clients.mindbodyonline.com/ASP/home.asp?studioid=8603"

    #Load Site into browser
    LoadUrl(scraper).run(url=url)

    #Wait for an iframe to load
    WaitForFrame(scraper).run(frame_name="mainFrame")

    #Click on a tab button (if necessary
    #ClickLink(scraper).run(link_text='Classes')  #ClickLink(scraper).run(link_text='MY INFO\')

    #get html content
    html = ReadPageContent(scraper).run()

    #get snippet with Schedule
    schedule_html = ExtractHtmlSnippet(scraper).run(html, "#classSchedule-mainTable") #"#classSchedule-mainTable tr"

    #TODO: validate that headers on the page match configured ones

    #expected_headers = dict()
    #expected_headers[ScraperOld.START_TIME] = 'Start time'
    #expected_headers[ScraperOld.CLASS_NAME] = 'Classes'
    #expected_headers[ScraperOld.TEACHER_NAME] = 'Teacher'
    #expected_headers[ScraperOld.DURATION] = 'Duration'


    actual_headers = list()
    actual_headers.append(ScraperOld.START_TIME) # = 'Start time'
    actual_headers.append("sign-up")
    actual_headers.append(ScraperOld.CLASS_NAME) # = 'Classes'
    actual_headers.append(ScraperOld.TEACHER_NAME) # = 'Teacher'
    actual_headers.append(ScraperOld.DURATION) # = 'Duration'


    parsed_events = ExtractEventsFromMBO(scraper).run(schedule_html, actual_headers)
    print "parsed events are: "+repr(parsed_events)

    #check that we successfully parsed the page

    #prepare new events for saving to DB
    studio = Studio.objects.get(pk=12)
    db_events = PrepareEventsForDB(scraper).run(studio,parsed_events)

    #map to known instructors.
    LinkToKnownInstructors(scraper).run(db_events)

    #validate that all prepared events will be accepted by DB (call db_event[i].full_clean() to verify)

    #delete events from DB

    #add new events to DB



    #load Next Weeks's scehedule
    ClickElement(scraper).run("week-arrow-r")

    #Wait for a certain element to load
    WaitForFrame(scraper).run(frame_name="mainFrame")

    #get html content
    html = ReadPageContent(scraper).run()

    #get snippet with Schedule
    schedule_html = ExtractHtmlSnippet(scraper).run(html, "#classSchedule-mainTable") #"#classSchedule-mainTable tr"
    print "that was second week's schedule"



    # Parse Events:
    #   define unique key: date+time, parsing source, scan number, studio, instructor,
    #
    # model:
    #   sources


    logger.debug('At the end of script: refresh')