import logging

logger = logging.getLogger(__name__)

class LoadUrl:

    def __init__(self, scraper):
        self.scraper = scraper


    def run(self, url):
        #self.scraper.browser.implicitly_wait(10)
        logger.debug("loading into browser URL: "+url)
        self.scraper.browser.get(url)
