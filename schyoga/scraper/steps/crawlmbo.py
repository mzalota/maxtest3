import logging
import datetime
from schyoga.scraper.steps.clickelement import ClickElement
from schyoga.scraper.steps.clicklink import ClickLink
from schyoga.scraper.steps.extracthtmlsnippet import ExtractHtmlSnippet
from schyoga.scraper.steps.loadurl import LoadUrl
from schyoga.scraper.steps.readpagecontent import ReadPageContent
from schyoga.scraper.steps.savehtmltodb import SaveHtmlToDB
from schyoga.scraper.steps.waitforframe import WaitForFrame


logger = logging.getLogger(__name__)

class CrawlMBO:
    NUMBER_OF_WEEKS_TO_CRAWL = 3

    def __init__(self, scraper):
        self.scraper = scraper


    def run(self, studio, mbol_studio_id, num_of_weeks, click_tab_name=None):
        """

        @type studio: Studio
        """
        mbol_studio_id = str(mbol_studio_id)

        if not num_of_weeks:
            num_of_weeks = self.NUMBER_OF_WEEKS_TO_CRAWL

        logger.debug("Starting to crawl MindBodyOnline site for studio: id: "+mbol_studio_id+", num_of_weeks: "+str(num_of_weeks))

        schedule_url = "https://clients.mindbodyonline.com/ASP/home.asp?studioid="+mbol_studio_id

        result = self.crawl_once(studio, schedule_url, num_of_weeks, click_tab_name)
        if not result:
            logger.warn("Could not locate #classSchedule-mainTable element on the page. Rerunning Crawler")
            result = self.crawl_once(studio, schedule_url, num_of_weeks, click_tab_name)
            if not result:
                logger.error("Even after reruning Crawler still could not locate #classSchedule-mainTable element on the page ")

        logger.debug("Finished Crawling MindBodyOnline site for studio: id: "+mbol_studio_id+", num_of_weeks: "+str(num_of_weeks))


    def crawl_once(self, studio, schedule_url, num_of_weeks, click_tab_name):
        """

        @type studio: Studio
        """

        LoadUrl(self.scraper).run(url=schedule_url)

        if click_tab_name:
            WaitForFrame(self.scraper).run(frame_name='mainFrame')
            ClickLink(self.scraper).run(link_text=click_tab_name)

        db_logs = list()
        processing_page = 1
        while int(num_of_weeks) >= processing_page:

            if processing_page > 1:
                ClickElement(self.scraper).run('week-arrow-r')

            WaitForFrame(self.scraper).run(frame_name='mainFrame')

            html1 = ReadPageContent(self.scraper).run()

            schedule_html = ExtractHtmlSnippet(self.scraper).run(html1, '#classSchedule-mainTable')
            if not schedule_html or len(schedule_html)<=0:
                logger.error("Could not locate #classSchedule-mainTable element on the page")
                return False

            current_week = datetime.datetime.now().isocalendar()[1]
            comment = 'week_'+str(current_week+(processing_page-1))
            parsing_history = SaveHtmlToDB(self.scraper).run(studio, comment, schedule_html)
            db_logs.append(parsing_history)

            processing_page += 1

        #each week was processes successfully. Save Parsing_History objects to DB
        for parsing_history in db_logs:
            parsing_history.save()

        return True