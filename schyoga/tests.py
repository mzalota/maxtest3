#from unittest import TestCase
from django.test import TestCase
from maxtest3.settings import local
from schyoga.bizobj.parser.scraper import Scraper
from schyoga.models import Parsing_History
import os.path

import schyoga

#PROJECT_ROOT = os.path.abspath(schyoga.__path__)

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
        htmlText = self.load_html_from_file("atmananda-yoga-sequence.html")

        expected_headers = dict()
        expected_headers[Scraper.START_TIME] = 'Start time'
        expected_headers[Scraper.CLASS_NAME] = 'classes'
        expected_headers[Scraper.TEACHER_NAME] = 'Teacher'
        expected_headers[Scraper.DURATION] = 'Duration'

        scraper = Scraper()

        #ACT
        events = scraper.parse(htmlText, expected_headers)

        ##ASSERT
        self.assertIsNotNone(scraper.mainTable)
        self.assertGreater(len(scraper.mainTable), 6) #check that the mainTablee has ~7 elements

        self.assertIsNotNone(events)
        self.assertEqual(len(events), 37)

    def test_run_bikram_yoga_grand_central(self):

        #ARRANGE
        htmlText = self.load_html_from_file("bikram-yoga-grand-central.html")

        expected_headers = dict()
        expected_headers[Scraper.START_TIME] = 'Start time'
        expected_headers[Scraper.CLASS_NAME] = 'Classes'
        expected_headers[Scraper.TEACHER_NAME] = 'Teacher'
        expected_headers[Scraper.DURATION] = 'Duration'

        scraper = Scraper()

        #ACT
        events = scraper.parse(htmlText, expected_headers)

        ##ASSERT
        self.assertIsNotNone(scraper.mainTable)
        self.assertGreater(len(scraper.mainTable), 6) #check that the mainTablee has ~7 elements

        self.assertIsNotNone(events)
        self.assertEqual(len(events), 43)


    def test_run_ashtanga_yoga_upper_west_side(self):

        #ARRANGE
        htmlText = self.load_html_from_file("ashtanga-yoga-upper-west-side.html")

        expected_headers = dict()
        expected_headers[Scraper.START_TIME] = 'Start time'
        expected_headers[Scraper.CLASS_NAME] = 'Classes'
        expected_headers[Scraper.TEACHER_NAME] = 'Teacher'
        expected_headers[Scraper.DURATION] = 'Duration'

        scraper = Scraper()

        #ACT
        events = scraper.parse(htmlText, expected_headers)

        ##ASSERT
        self.assertIsNotNone(scraper.mainTable)
        self.assertGreater(len(scraper.mainTable), 6) #check that the mainTablee has ~7 elements

        self.assertIsNotNone(events)
        self.assertEqual(len(events), 9)


    def test_run_abhayayoga(self):

        #ARRANGE
        htmlText = self.load_html_from_file("abhayayoga.html")

        expected_headers = dict()
        expected_headers[Scraper.START_TIME] = 'Start time'
        expected_headers[Scraper.CLASS_NAME] = 'Classes'
        expected_headers[Scraper.TEACHER_NAME] = 'Teacher'
        expected_headers[Scraper.DURATION] = 'Duration'

        scraper = Scraper()

        #ACT
        events = scraper.parse(htmlText, expected_headers)

        ##ASSERT
        self.assertIsNotNone(scraper.mainTable)
        self.assertGreater(len(scraper.mainTable), 6) #check that the mainTablee has ~7 elements

        self.assertIsNotNone(events)
        self.assertEqual(len(events), 37)


    def test_run_bend_and_bloom_yoga(self):

        #ARRANGE
        htmlText = self.load_html_from_file("bend-and-bloom-yoga.html")

        expected_headers = dict()
        expected_headers[Scraper.START_TIME] = 'Start time'
        expected_headers[Scraper.CLASS_NAME] = 'Classes'
        expected_headers[Scraper.TEACHER_NAME] = 'Teacher'
        expected_headers[Scraper.DURATION] = 'Duration'

        scraper = Scraper()

        #ACT
        events = scraper.parse(htmlText, expected_headers)

        ##ASSERT
        self.assertIsNotNone(scraper.mainTable)
        self.assertGreater(len(scraper.mainTable), 6) #check that the mainTablee has ~7 elements

        self.assertIsNotNone(events)
        self.assertEqual(len(events), 62)
