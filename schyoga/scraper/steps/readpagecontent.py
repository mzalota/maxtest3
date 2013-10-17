import logging


logger = logging.getLogger(__name__)

class ReadPageContent:
    def __init__(self, scraper):
        self.scraper = scraper

    def run(self):
        logger.debug("returning page source: ")
        return self.scraper.browser.page_source
