import logging

logger = logging.getLogger(__name__)


class ClickElement:
    def __init__(self, scraper):
        self.scraper = scraper

    def run(self, element_id):
        try:
            logger.debug("Clicking on element: " + element_id)
            element = self.scraper.browser.find_element_by_id(element_id)
        except:
            logger.debug("Could not find element: " + element_id + " for clicking")
            return False

        try:
            element.click()
            return True
        except:
            logger.debug("Could not click on element: " + element_id)
            return False
