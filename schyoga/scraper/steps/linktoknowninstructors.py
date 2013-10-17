import logging

logger = logging.getLogger(__name__)

class LinkToKnownInstructors:

    def __init__(self, scraper):
        self.scraper = scraper


    def run(self, db_events):
        logger.debug("Linking events to known instructors")