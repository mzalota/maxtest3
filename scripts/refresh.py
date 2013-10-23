import logging
from schyoga.bizobj.parser.scraperOld import ScraperOld
from schyoga.models import Event, Instructor
from schyoga.scraper.scraper import Scraper
from schyoga.scraper.steps.clickelement import ClickElement
from schyoga.scraper.steps.clicklink import ClickLink
from schyoga.scraper.steps.extracteventsfrommbo import ExtractEventsFromMBO
from schyoga.scraper.steps.extracthtmlsnippet import ExtractHtmlSnippet
from schyoga.scraper.steps.linktoknowninstructors import LinkToKnownInstructors
from schyoga.scraper.steps.loadurl import LoadUrl
from schyoga.scraper.steps.prepareeventsfordb import PrepareEventsForDB
from schyoga.scraper.steps.readpagecontent import ReadPageContent
from schyoga.scraper.steps.standardizeinstructornames import StandardizeInstructorNames
from schyoga.scraper.steps.waitforelement import WaitForElement
from schyoga.scraper.steps.waitforframe import WaitForFrame

from schyoga.models import Studio

logger = logging.getLogger(__name__)

class SiteConfig:
    url = "http://clients.mindbodyonline.com/ws.asp?studioid=9882"
    steps = dict({'load_url': "http://clients.mindbodyonline.com/ws.asp?studioid=9882",
                  'switch_to_tab':'CLASSES',
                  'headers': list([ScraperOld.START_TIME, 'sign-up', ScraperOld.CLASS_NAME, ScraperOld.TEACHER_NAME,ScraperOld.DURATION]),
                  'studio_id': '12'})

    steps2 = list([dict({'step_name':'LoadUrl',
                         'url':"https://clients.mindbodyonline.com/ASP/ws.asp?studioid=5782"}),
                    dict({'step_name': 'WaitForFrame',
                         'frame_name':"mainFrame"}),
                    dict({'step_name':'ReadPageContent',
                         'return_var_name': 'html1'}),
                    dict({'step_name':'ExtractHtmlSnippet',
                         'html_var_name': 'html1',
                         'element_id': '#classSchedule-mainTable',
                         'return_var_name': 'schedule_html'}),
                    dict({'step_name':'ExtractEventsFromMBO',
                         'html_var_name': 'schedule_html',
                         'headers': list([ScraperOld.START_TIME, 'sign-up', ScraperOld.CLASS_NAME, ScraperOld.TEACHER_NAME,'assistant',ScraperOld.DURATION]),
                         'return_var_name': 'parsed_events'}),
                    dict({'step_name':'PrepareEventsForDB',
                          'parsed_events_var_name': 'parsed_events',
                          'return_var_name': 'db_events'}),
                    dict({'step_name':'StandardizeInstructorNames',
                          'db_events_var_name': 'db_events',
                          'return_var_name': 'instructors_standard'}),
                    dict({'step_name':'LinkToKnownInstructors',
                          'instructors_standard_var_name': 'instructors_standard',
                          'return_var_name': 'instructors_matched'}),


                   # dict({'step_name':'ClickElement',
                   #      'element_id': 'week-arrow-r'}),
                   # dict({'step_name': 'WaitForFrame',
                   #      'frame_name':"mainFrame"}),
                   # dict({'step_name':'ReadPageContent',
                   #      'return_var_name': 'html2'}),
                   # dict({'step_name':'ExtractHtmlSnippet',
                   #      'html_var_name': 'html2',
                   #      'element_id': '#classSchedule-mainTable',
                   #      'return_var_name': 'schedule_html2'}),
                   # dict({'step_name':'ExtractEventsFromMBO',
                   #      'html_var_name': 'schedule_html2',
                   #      'headers': list([ScraperOld.START_TIME, 'sign-up', ScraperOld.CLASS_NAME, ScraperOld.TEACHER_NAME,'assistant',ScraperOld.DURATION]),
                   #      'return_var_name': 'parsed_events2'}),
                   # dict({'step_name':'PrepareEventsForDB',
                   #       'parsed_events_var_name': 'parsed_events2',
                   #       'return_var_name': 'db_events2'}),
                   ])


    steps4 = list([dict({'step_name':'LoadUrl',
                         'url':"http://clients.mindbodyonline.com/ws.asp?studioid=17"}),
                    dict({'step_name': 'WaitForFrame',
                         'frame_name':"mainFrame"}),
                    dict({'step_name':'ReadPageContent',
                         'return_var_name': 'html1'}),
                    dict({'step_name':'ExtractHtmlSnippet',
                         'html_var_name': 'html1',
                         'element_id': '#classSchedule-mainTable',
                         'return_var_name': 'schedule_html'}),
                    dict({'step_name':'ExtractEventsFromMBO',
                         'html_var_name': 'schedule_html',
                         'headers': list([ScraperOld.START_TIME, 'sign-up', ScraperOld.CLASS_NAME, ScraperOld.TEACHER_NAME,ScraperOld.DURATION]),
                         'return_var_name': 'parsed_events'}),
                    dict({'step_name':'PrepareEventsForDB',
                          'parsed_events_var_name': 'parsed_events',
                          'return_var_name': 'db_events'}),

                    dict({'step_name':'ClickElement',
                         'element_id': 'week-arrow-r'}),
                    dict({'step_name': 'WaitForFrame',
                         'frame_name':"mainFrame"}),
                    dict({'step_name':'ReadPageContent',
                         'return_var_name': 'html2'}),
                    dict({'step_name':'ExtractHtmlSnippet',
                         'html_var_name': 'html2',
                         'element_id': '#classSchedule-mainTable',
                         'return_var_name': 'schedule_html2'}),
                    dict({'step_name':'ExtractEventsFromMBO',
                         'html_var_name': 'schedule_html2',
                         'headers': list([ScraperOld.START_TIME, 'sign-up', ScraperOld.CLASS_NAME, ScraperOld.TEACHER_NAME,ScraperOld.DURATION]),
                         'return_var_name': 'parsed_events2'}),
                    dict({'step_name':'PrepareEventsForDB',
                          'parsed_events_var_name': 'parsed_events2',
                          'return_var_name': 'db_events2'}),
                   ])


    steps3 = list([dict({'step_name':'LoadUrl',
                         'url':"http://clients.mindbodyonline.com/ws.asp?studioid=9882"}),
                    dict({'step_name': 'WaitForFrame',
                         'frame_name':"mainFrame"}),
                    dict({'step_name':'ClickLink',
                         'link_text': 'CLASSES'}),
                    dict({'step_name':'ReadPageContent',
                         'return_var_name': 'html1'}),
                    dict({'step_name':'ExtractHtmlSnippet',
                         'html_var_name': 'html1',
                         'element_id': '#classSchedule-mainTable',
                         'return_var_name': 'schedule_html'}),
                    dict({'step_name':'ExtractEventsFromMBO',
                         'html_var_name': 'schedule_html',
                         'headers': list([ScraperOld.START_TIME, 'sign-up', ScraperOld.CLASS_NAME, ScraperOld.TEACHER_NAME,ScraperOld.DURATION]),
                         'return_var_name': 'parsed_events'}),
                    dict({'step_name':'PrepareEventsForDB',
                          'parsed_events_var_name': 'parsed_events',
                          'return_var_name': 'db_events'}),

                    dict({'step_name':'ClickElement',
                         'element_id': 'week-arrow-r'}),
                    dict({'step_name': 'WaitForFrame',
                         'frame_name':"mainFrame"}),
                    dict({'step_name':'ReadPageContent',
                         'return_var_name': 'html2'}),
                    dict({'step_name':'ExtractHtmlSnippet',
                         'html_var_name': 'html2',
                         'element_id': '#classSchedule-mainTable',
                         'return_var_name': 'schedule_html2'}),
                    dict({'step_name':'ExtractEventsFromMBO',
                         'html_var_name': 'schedule_html2',
                         'headers': list([ScraperOld.START_TIME, 'sign-up', ScraperOld.CLASS_NAME, ScraperOld.TEACHER_NAME,ScraperOld.DURATION]),
                         'return_var_name': 'parsed_events2'}),
                    dict({'step_name':'PrepareEventsForDB',
                          'parsed_events_var_name': 'parsed_events2',
                          'return_var_name': 'db_events2'}),
                   ])


def run():

    logger.debug("starting script: refresh")

    site_config = SiteConfig()

    scraper = Scraper()

    studio_id = 12
    studio = Studio.objects.get(pk=studio_id)

    for step in site_config.steps2:
        if step['step_name'] == 'LoadUrl':
            LoadUrl(scraper).run(url=step['url'])
        if step['step_name'] == 'WaitForFrame':
            WaitForFrame(scraper).run(frame_name=step['frame_name'])
        if step['step_name'] == 'ClickLink':
            ClickLink(scraper).run(link_text=step['link_text'])
        if step['step_name'] == 'ReadPageContent':
            result = ReadPageContent(scraper).run()
            scraper.vars[step['return_var_name']] = result
        if step['step_name'] == 'ExtractHtmlSnippet':
            html_str = scraper.vars[step['html_var_name']]
            result = ExtractHtmlSnippet(scraper).run(html_str, step['element_id'])
            scraper.vars[step['return_var_name']] = result
        if step['step_name'] == 'ExtractEventsFromMBO':
            html_str = scraper.vars[step['html_var_name']]
            result = ExtractEventsFromMBO(scraper).run(html_str, step['headers'])
            scraper.vars[step['return_var_name']] = result
        if step['step_name'] == 'PrepareEventsForDB':
            parsed_events = scraper.vars[step['parsed_events_var_name']]
            result = PrepareEventsForDB(scraper).run(studio,parsed_events)
            scraper.vars[step['return_var_name']] = result
        if step['step_name'] == 'ClickElement':
            ClickElement(scraper).run(step['element_id'])

        if step['step_name'] == 'StandardizeInstructorNames':
            db_events = scraper.vars[step['db_events_var_name']]
            instructors_raw = set(db_event.instructor_name for db_event in db_events)
            result = StandardizeInstructorNames(scraper).run(instructors_raw)
            scraper.vars[step['return_var_name']] = result

        if step['step_name'] == 'LinkToKnownInstructors':
            #db_events = scraper.vars[step['db_events_var_name']]
            instructors_standard = scraper.vars[step['instructors_standard_var_name']]
            result = LinkToKnownInstructors(scraper).run(studio.instructors, instructors_standard)
            scraper.vars[step['return_var_name']] = result

        if step['step_name'] == 'SaveUnmatchedInstructorsToDB':
            instructors_matched = scraper.vars[step['instructors_matched_var_name']]
            instructors_unmatched = set(instructors_standard.keys()) - set(instructors_matched.keys())
            instructors_added = dict()
            for instructor_name in instructors_unmatched:
                new_instructor = Instructor()
                new_instructor.instructor_name = instructor_name
                instructors_added[instructor_name] = new_instructor


    logger.debug("Parsed Out DB Events 1111 are :")
    db_events = scraper.vars['db_events']
    for idx, db_event in enumerate(db_events):
        logger.debug( str(idx)+": "+db_event.comments + ", "+repr(db_event.start_time)+", "+db_event.instructor_name)


    logger.debug("Parsed Out DB Events 2222 are :")
    db_events2 = scraper.vars['db_events2']
    for idx, db_event in enumerate(db_events2):
        logger.debug( str(idx)+": "+db_event.comments + ", "+repr(db_event.start_time)+", "+db_event.instructor_name)

    logger.debug("done with the switch statement")

    return


    #TODO: validate that headers on the page match configured ones


    #TODO: check that we successfully parsed the page



    #map to known instructors.
    LinkToKnownInstructors(scraper).run(db_events)

    #validate that all prepared events will be accepted by DB (call db_event[i].full_clean() to verify)

    #delete events from DB

    #add new events to DB



    # Parse Events:
    #   define unique key: date+time, parsing source, scan number, studio, instructor,
    #
    # model:
    #   sources


    logger.debug('At the end of script: refresh')