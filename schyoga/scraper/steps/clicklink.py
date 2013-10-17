import logging


logger = logging.getLogger(__name__)

class ClickLink:

    def __init__(self, scraper):
        self.scraper = scraper


    def run(self, link_text):
        logger.debug("Clicking on link with text: "+link_text)
        self.scraper.browser.find_element_by_partial_link_text(link_text).click()
        logger.debug("Finished with clicking on link with text: "+link_text)
