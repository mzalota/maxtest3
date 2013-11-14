import logging
import datetime
from django.core import serializers
from schyoga.bizobj.parser.scraperOld import ScraperOld
from schyoga.models import Event, Instructor
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

from schyoga.models import Studio
import io, json
import codecs

logger = logging.getLogger(__name__)

class SiteConfig:
    url = "http://clients.mindbodyonline.com/ws.asp?studioid=9882"
    steps = dict({'load_url': "http://clients.mindbodyonline.com/ws.asp?studioid=9882",
                  'switch_to_tab':'CLASSES',
                  'headers': list([ScraperOld.START_TIME, 'sign-up', ScraperOld.CLASS_NAME, ScraperOld.TEACHER_NAME,ScraperOld.DURATION]),
                  'studio_id': '12'})

    steps5 = list([dict({'step_name': 'MBOLReadHtml',
                         'mbol_studio_id': "5782",
                         'click_tab_name': 'CLASSES',
                         'num_of_weeks': '2', })
                   ])

    steps2 = list([dict({'step_name': 'LoadUrl',
                         'url': "https://clients.mindbodyonline.com/ASP/ws.asp?studioid=5782"}),
                    dict({'step_name': 'WaitForFrame',
                         'frame_name': "mainFrame"}),
                    dict({'step_name': 'ReadPageContent',
                         'return_var_name': 'html1'}),
                    dict({'step_name': 'ExtractHtmlSnippet',
                         'html_var_name': 'html1',
                         'element_id': '#classSchedule-mainTable',
                         'return_var_name': 'schedule_html'}),
                    dict({'step_name': 'ExtractEventsFromMBO',
                         'html_var_name': 'schedule_html',
                         'headers': list([ScraperOld.START_TIME, 'sign-up', ScraperOld.CLASS_NAME, ScraperOld.TEACHER_NAME,'assistant',ScraperOld.DURATION]),
                         'return_var_name': 'parsed_events'}),
                    dict({'step_name': 'PrepareEventsForDB',
                          'parsed_events_var_name': 'parsed_events',
                          'return_var_name': 'db_events'}),
                    dict({'step_name': 'LinkToKnownInstructors',
                          'db_events_var_name': 'db_events',
                          'return_var_name': 'instructors_unmatched'}),
                    dict({'step_name': 'DealWithNewInstructors',
                          'instructors_unmatched_var_name': 'instructors_unmatched',
                          'file_path': "C:/tmp/unknown_instructors.cvs"}),


                    #dict({'step_name':'StandardizeInstructorNames',
                    #      'db_events_var_name': 'db_events',
                    #      'return_var_name': 'instructors_standard'}),
                    #dict({'step_name':'LinkToKnownInstructors',
                    #      'instructors_standard_var_name': 'instructors_standard',
                    #      'return_var_name': 'instructors_matched'}),


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



    #with io.open('c:/tmp/json_data.txt', 'w', encoding='utf-8') as f:
    #    f.write(unicode(json.dumps(site_config.steps2, ensure_ascii=False, indent=2)))
    #
    #logger.debug("loading data from json file: ")
    #with open('c:/tmp/json_data.txt') as data_file:
    #    data = json.load(data_file)
    #print repr(data)


#TODO: V.2. deal with YogaNesh schedule - it has extra rows with "Yoga" or "Dance" heading in the first column
#TODO V.2. deal with case when  there is "no scheduled classes or training sessions" messaage in calendar e.g. for "Yoga Union Center For Backcare & Scoliosis"

def run():

    logger.debug("starting script: refresh")

    #7, 53

    scraper = Scraper()
    studios = Studio.objects.all().filter(id__gte=1).filter(id__lte=200).order_by('id')
    for studio in studios:
        process_studio(scraper, studio)

    logger.debug('At the end of script: refresh')


def process_studio(scraper, studio):

    logger.debug("processing studio: "+str(studio.id)+", "+studio.name)

    studio_site_set = studio.studio_site_set.all()
    if not studio_site_set:
        logger.error("Config data is not specified for studio: "+str(studio.id)+", "+studio.name)
        return

    if len(studio_site_set)>1:
        logger.error("More then one Studio_Site object exists for  studio: "+str(studio.id)+", "+studio.name)
        return


    #config_crawl_json = studio_site_set[0].config_crawl
    #config_crawl = json.loads(config_crawl_json)
    #for step in config_crawl:
    #    process_step(step, scraper, studio)

    config_parse_json = studio_site_set[0].config_parse
    if not config_parse_json or (len(config_parse_json)) <=0:
        logger.error("No Parse Config found! Skipping studio: "+str(studio.id)+", "+studio.name)
        return

    config_parse = json.loads(config_parse_json)
    for step in config_parse:
        process_step(step, scraper, studio)

    #logger.debug("Parsed Out DB Events 1111 are :")
    #db_events = scraper.vars['db_events']
    #for idx, db_event in enumerate(db_events):
    #    logger.debug( str(idx)+": "+db_event.comments + ", "+repr(db_event.start_time)+", "+db_event.instructor_name)


    #logger.debug("Parsed Out DB Events 2222 are :")
    #db_events2 = scraper.vars['db_events2']
    #for idx, db_event in enumerate(db_events2):
    #    logger.debug( str(idx)+": "+db_event.comments + ", "+repr(db_event.start_time)+", "+db_event.instructor_name)

    logger.debug("done with the switch statement")


    #TODO: Keep track of Assistants. They soon will become teachers (or may be teachig elsewhere). co-Teacher. Assistant2, Acompanist, etc.
    #TODO: validate that headers on the page match configured ones
    #TODO: check that we successfully parsed the page



    # Parse Events:
    #   define unique key: date+time, parsing source, scan number, studio, instructor,
    #
    # model:
    #   sources


def parsing_html(headers, html_str, instructors_file_path, scraper, studio):

    parsed_events = ExtractEventsFromMBO(scraper).run(html_str, headers)
    db_events = PrepareEventsForDB(scraper).run(studio, parsed_events)
    studio_instructors = studio.instructors.all()
    instructors_unmatched = LinkToKnownInstructors(scraper).run2(studio_instructors, db_events)
    DealWithNewInstructors(scraper).run(studio, instructors_unmatched, instructors_file_path)

    scraper.vars['db_events'] = db_events
    if db_events:
        json_db_events = serializers.serialize('json', db_events)
        #print json_db_events

    return db_events


        #if step['step_name'] == 'SaveUnmatchedInstructorsToDB':
        #    instructors_matched = scraper.vars[step['instructors_matched_var_name']]
        #    instructors_unmatched = set(instructors_standard.keys()) - set(instructors_matched.keys())
        #    instructors_added = dict()
        #    for instructor_name in instructors_unmatched:
        #        new_instructor = Instructor()
        #        new_instructor.instructor_name = instructor_name
        #        instructors_added[instructor_name] = new_instructor


def process_step(step, scraper, studio):
    logger.debug("Processing step: "+step['step_name'])

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

    if step['step_name'] == 'SaveHtmlToDB':
        html_text = scraper.vars[step['html_var_name']]
        SaveHtmlToDB(scraper).run(studio, step['comment'], html_text)

    if step['step_name'] == 'LinkToKnownInstructors':
        db_events = scraper.vars[step['db_events_var_name']]
        studio_instructors = studio.instructors.all()
        result = LinkToKnownInstructors(scraper).run2(studio_instructors, db_events)
        scraper.vars[step['return_var_name']] = result
        #print repr(result)

    if step['step_name'] == 'DealWithNewInstructors':
        instructors_unmatched = scraper.vars[step['instructors_unmatched_var_name']]
        DealWithNewInstructors(scraper).run(studio, instructors_unmatched, step['file_path'])

    if step['step_name'] == 'MBOLReadHtml':
        mbol_studio_id = step['mbol_studio_id']
        schedule_url = "https://clients.mindbodyonline.com/ASP/home.asp?studioid="+mbol_studio_id
        num_of_weeks = step.get('num_of_weeks', "2")
        click_tab_name = step.get('click_tab_name', None)

        logger.debug("Processing MindBodyOnline studioid: "+mbol_studio_id+", num_of_weeks: "+num_of_weeks)

        LoadUrl(scraper).run(url=schedule_url)
        if click_tab_name:
            WaitForFrame(scraper).run(frame_name='mainFrame')
            ClickLink(scraper).run(link_text=click_tab_name)

        processing_page = 1
        while int(num_of_weeks) >= processing_page:

            if processing_page > 1:
                ClickElement(scraper).run('week-arrow-r')
            WaitForFrame(scraper).run(frame_name='mainFrame')
            html1 = ReadPageContent(scraper).run()
            schedule_html = ExtractHtmlSnippet(scraper).run(html1, '#classSchedule-mainTable')

            current_week = datetime.datetime.now().isocalendar()[1]
            comment = 'week_'+str(current_week+(processing_page-1))

            if not schedule_html or len(schedule_html)<=0:
                logger.error("Could not locate #classSchedule-mainTable element on the page")
                SaveHtmlToDB(scraper).run(studio, comment, html1)
            else:
                SaveHtmlToDB(scraper).run(studio, comment, schedule_html)


            processing_page = processing_page + 1

    if step['step_name'] == 'MBOLParseHtml':
        headers = step['headers']
        instructors_file_path = "C:/tmp/unknown_instructors.cvs" #step['file_path']

        logger.debug("Parsing events out of MindBodyOnline HTML")

        #load from parsing_history
        current_week_num = datetime.datetime.now().isocalendar()[1]
        wk1 = 'week_'+str(current_week_num)
        wk2 = 'week_'+str(current_week_num+1)

        #htmls = studio.parsing_history_set.filter(comment__in=['week_1', 'week_2'])
        htmls = studio.parsing_history_set.filter(comment__in=[wk1, wk2])
        if not htmls or len(htmls) <= 0:
            logger.error("No parsed_history objects found ")
            return

        #TODO: delete events for this studio from DB

        for html in htmls:
            html_str = html.calendar_html
            db_events = parsing_html(headers, html_str, instructors_file_path, scraper, studio)

            if db_events:
                for db_event in db_events:
                    db_event.save()

