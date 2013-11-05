#from unittest import TestCase
from django.db import connection
from django.test import TestCase
from mock import patch, Mock
from schyoga.bizobj.parser.scraperOld import ScraperOld
from schyoga.models import Parsing_History, Event, Studio, Instructor
import os.path
from dateutil import parser

import schyoga

#PROJECT_ROOT = os.path.abspath(schyoga.__path__)
from schyoga.scraper.scraper import Scraper
from schyoga.scraper.steps.linktoknowninstructors import LinkToKnownInstructors
from schyoga.scraper.steps.prepareeventsfordb import PrepareEventsForDB
from schyoga.scraper.steps.standardizeinstructornames import StandardizeInstructorNames


class ScraperTestCase(TestCase):
    def setUp(self):
        pass

    def load_html_from_file(self, file_name):
        resources_dir = schyoga.__path__[0] + "\\resources"
        path = resources_dir + "\\"+file_name
        with open(path) as myfile:
            htmlText = myfile.read()
        return htmlText

    def test_run(self):

        #ARRANGE
        htmlText = self.load_html_from_file("13_atmananda-yoga-sequence.html")

        expected_headers = dict()
        expected_headers[ScraperOld.START_TIME] = 'Start time'
        expected_headers[ScraperOld.CLASS_NAME] = 'classes'
        expected_headers[ScraperOld.TEACHER_NAME] = 'Teacher'
        expected_headers[ScraperOld.DURATION] = 'Duration'

        scraper = ScraperOld()

        #ACT
        events = scraper.parse(htmlText, expected_headers)

        ##ASSERT
        self.assertIsNotNone(scraper.mainTable)
        self.assertGreater(len(scraper.mainTable), 6) #check that the mainTablee has ~7 elements

        self.assertIsNotNone(events)
        self.assertEqual(len(events), 37)

    def test_run_bikram_yoga_grand_central(self):

        #ARRANGE
        htmlText = self.load_html_from_file("17_bikram-yoga-grand-central.html")

        expected_headers = dict()
        expected_headers[ScraperOld.START_TIME] = 'Start time'
        expected_headers[ScraperOld.CLASS_NAME] = 'Classes'
        expected_headers[ScraperOld.TEACHER_NAME] = 'Teacher'
        expected_headers[ScraperOld.DURATION] = 'Duration'

        scraper = ScraperOld()

        #ACT
        events = scraper.parse(htmlText, expected_headers)

        ##ASSERT
        self.assertIsNotNone(scraper.mainTable)
        self.assertGreater(len(scraper.mainTable), 6) #check that the mainTablee has ~7 elements

        self.assertIsNotNone(events)
        self.assertEqual(len(events), 43)


    def test_run_ashtanga_yoga_upper_west_side(self):

        #ARRANGE
        htmlText = self.load_html_from_file("12_ashtanga-yoga-upper-west-side.html")

        expected_headers = dict()
        expected_headers[ScraperOld.START_TIME] = 'Start time'
        expected_headers[ScraperOld.CLASS_NAME] = 'Classes'
        expected_headers[ScraperOld.TEACHER_NAME] = 'Teacher'
        expected_headers[ScraperOld.DURATION] = 'Duration'

        scraper = ScraperOld()

        #ACT
        events = scraper.parse(htmlText, expected_headers)

        ##ASSERT
        self.assertIsNotNone(scraper.mainTable)
        self.assertGreater(len(scraper.mainTable), 6) #check that the mainTablee has ~7 elements

        self.assertIsNotNone(events)
        self.assertEqual(len(events), 9)


    def test_run_abhayayoga(self):

        #ARRANGE
        htmlText = self.load_html_from_file("7_abhayayoga.html")

        expected_headers = dict()
        expected_headers[ScraperOld.START_TIME] = 'Start time'
        expected_headers[ScraperOld.CLASS_NAME] = 'Classes'
        expected_headers[ScraperOld.TEACHER_NAME] = 'Teacher'
        expected_headers[ScraperOld.DURATION] = 'Duration'

        scraper = ScraperOld()

        #ACT
        events = scraper.parse(htmlText, expected_headers)

        ##ASSERT
        self.assertIsNotNone(scraper.mainTable)
        self.assertGreater(len(scraper.mainTable), 6) #check that the mainTablee has ~7 elements

        self.assertIsNotNone(events)
        self.assertEqual(len(events), 37)


    def test_run_bend_and_bloom_yoga(self):

        #ARRANGE
        htmlText = self.load_html_from_file("15_bend-and-bloom-yoga.html")

        expected_headers = dict()
        expected_headers[ScraperOld.START_TIME] = 'Start time'
        expected_headers[ScraperOld.CLASS_NAME] = 'Classes'
        expected_headers[ScraperOld.TEACHER_NAME] = 'Teacher'
        expected_headers[ScraperOld.DURATION] = 'Duration'


        scraper = ScraperOld()

        #ACT
        events = scraper.parse(htmlText, expected_headers)

        ##ASSERT
        self.assertIsNotNone(scraper.mainTable)
        self.assertGreater(len(scraper.mainTable), 6) #check that the mainTablee has ~7 elements

        self.assertIsNotNone(events)
        self.assertEqual(len(events), 62)


class PrepareEventsForDBTestCase(TestCase):

    def setUp(self):
        #Load data into schyoga_studio table for testing
        f = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../sql", "studio.sql"), "r")
        sql = f.read()
        cursor = connection.cursor()
        cursor.execute(sql)

        #following link explains why the data is not loaded into DB automatically when test is run as it would with syncdb
        #https://code.djangoproject.com/ticket/16550

    def test_run(self):

        #ARRANGE
        scraper = Scraper()
        step = PrepareEventsForDB(scraper)
        studio = Studio.objects.get(pk=12)
        parsed_events = [{'duration': u'3 hours', 'sign-up': '', 'teacher-name': u'Zoe and Ben', 'start-time': u'1:00 pm', 'class-name': u'Mysore', 'date': u'Fri October 25, 2013'},
                         {'date': u'Oct 1, 2013', 'duration': u'1.5 hour', 'sign-up': '', 'teacher-name': u'Zoe Benjamin', 'start-time': u'4:30 pm', 'class-name': u'Intro to Yoga'}]

        expected_datetime1 = parser.parse('2013-10-25 13:00:00')
        expected_datetime2 = parser.parse('2013-10-01 16:30:00')

        #ACT
        db_events = step.run(studio, parsed_events)

        ##ASSERT
        self.assertIsNotNone(db_events)
        self.assertEqual(len(db_events), 2)
        self.assertIsInstance(db_events[0], Event)
        self.assertEqual(db_events[0].start_time, expected_datetime1 )
        self.assertEqual(db_events[0].comments, 'Mysore')
        self.assertEqual(db_events[0].instructor_name, 'Zoe and Ben')

        self.assertIsInstance(db_events[1], Event)
        self.assertEqual(db_events[1].start_time, expected_datetime2 )
        self.assertEqual(db_events[1].comments, 'Intro to Yoga')
        self.assertEqual(db_events[1].instructor_name, 'Zoe Benjamin')


class StandardizeInstructorNamesTestCase(TestCase):

    def test_run(self):

        #ARRANGE
        scraper = Scraper()
        step = StandardizeInstructorNames(scraper)

        instructors_raw = set([u'Leslie Lewis (3)',
                               u'Lulu Ekiert',
                               u' lulu   ekiert ',
                               u'Ria Cooper',
                               u'Karrie Adamany',
                               u'Marisa Sullivan',
                               u'Katie Fraumann (4)',
                               u'Leslie Lewis',
                               u'Roaine Fine',
                               u'Erin Lewis',
                               u'Kate Filina',
                               u'Katie Fraumann',
                               u'Alana Kessler',
                               u'Katie Fraumann (1)',
                               u'Ashley Smith',
                               u'Ashley Smith (2)',
                               u'Aimee McCabe - Karr',
                               u'Jacob Hoffman'])

        #ACT
        instructors = step.run(instructors_raw)

        ##ASSERT
        self.assertIsNotNone(instructors)
        self.assertEqual(len(instructors), 18)
        self.assertEqual(len(set(instructors.values())),13)
        self.assertEqual(instructors[u' lulu   ekiert '], u'lulu-ekiert')
        self.assertIn(u'karrie-adamany', instructors.values())


    def test_run_remove_dashes(self):

        #ARRANGE
        scraper = Scraper()
        step = StandardizeInstructorNames(scraper)

        instructors_raw = set([u'Aimee McCabe - Karr'])

        #ACT
        instructors = step.run(instructors_raw)

        ##ASSERT
        self.assertIsNotNone(instructors)
        self.assertEqual(len(instructors), 1)
        self.assertEqual(len(set(instructors.values())),1)
        self.assertIn(u'aimee-mccabe-karr', instructors.values())


class LinkToKnownInstructorsTestCase(TestCase):

    def test_run(self):

        #ARRANGE
        scraper = Scraper()
        step = LinkToKnownInstructors(scraper)
        fakeObj = Instructor()
        fakeObj.name_url = 'aimee-mccabe-karr'
        studio_instructors = list([fakeObj])
        instructors = dict({u'Aimee McCabe - Karr':u'aimee-mccabe-karr',
                            u'Aimee McCabe - Karr (1)':u'aimee-mccabe-karr',
                            u'Kate Filina': u'kate-filina'})

        #ACT
        matched = step.run(studio_instructors, instructors)

        ##ASSERT
        self.assertIsNotNone(matched)
        self.assertEqual(len(matched), 2)
        self.assertEqual(matched[u'Aimee McCabe - Karr'],fakeObj)
        self.assertEqual(matched[u'Aimee McCabe - Karr (1)'],fakeObj)


    def test_run2(self):

        #ARRANGE
        scraper = Scraper()
        step = LinkToKnownInstructors(scraper)

        instructor_1 = Instructor()
        instructor_1.aliases_list = list(['Aimee McCabe - Karr', 'Aimee McCabe Karr'])
        instructor_2 = Instructor()
        instructor_2.aliases_list = list(['Kate Filina', 'Kate D Filina'])

        studio_instructors = list([instructor_1, instructor_2])

        event_1 = Event()
        event_1.instructor_name = 'Aimee McCabe - Karr'
        event_2 = Event()
        event_2.instructor_name = 'Nadya Zalota'
        event_3 = Event()
        event_3.instructor_name = 'Aimee McCabe Karr'
        event_4 = Event()
        event_4.instructor_name = 'Kate D Filina'

        db_events = list([event_1,event_2,event_3,event_4])

        #ACT
        unmatched = step.run2(studio_instructors, db_events)

        ##ASSERT
        self.assertIsNotNone(db_events)
        self.assertEqual(len(db_events), 4)
        self.assertIsNotNone(event_1.instructor)
        self.assertIsNone(event_2.instructor)
        self.assertIsNotNone(event_3.instructor)
        self.assertIsNotNone(event_4.instructor)

        self.assertIsNotNone(unmatched)
        self.assertEqual(len(unmatched), 1)