
import logging
from django.utils.encoding import smart_text
from schyoga.models import Parsing_History

logger = logging.getLogger(__name__)

class SaveHtmlToDB:

    def __init__(self, scraper):
        self.scraper = scraper

    def run(self, studio, comment, html_text):
        logger.debug("creating new parsing history obj")

        html_text = smart_text(html_text, encoding='utf-8', strings_only=False, errors='strict')

        #logger.debug("html text is:")
        #logger.debug(html_text)

        parHist = Parsing_History()
        parHist.studio = studio
        parHist.scrape_uuid = self.scraper.uuid
        parHist.comment = comment
        parHist.calendar_html = html_text #.decode('utf-8')
        parHist.save()