#from unittest import TestCase
from django.test import TestCase
from maxtest3.settings import local
from schyoga.bizobj.parser.scraperOld import ScraperOld
from schyoga.models import Parsing_History


class ScraperTestCase(TestCase):
    def setUp(self):
        pass

    def test_run(self):
        #ARRANGE

        #parHists = Parsing_History.objects.all()
        print "lenght of parHist objects is: "
        #print len(parHists)
        #parHist = Parsing_History.objects.get(pk=1)
        #htmlText = parHist.calendar_html
        #scraper = Scraper()

        #ACT
        #mainTable = scraper.parse(htmlText)

        #ASSERT
        #self.assertIsNotNone(mainTable)
        self.fail()