
import logging
from schyoga.models import Parsing_History

logger = logging.getLogger(__name__)

class SaveHtmlToDB:

    def __init__(self, scraper):
        self.scraper = scraper

    def run(self, studio, comment, html_text):
        logger.debug("creating new parsing history obj")
        parHist = Parsing_History()
        parHist.studio = studio
        parHist.scrape_uuid = self.scraper.uuid
        parHist.comment = comment
        parHist.calendar_html = html_text
        parHist.save()