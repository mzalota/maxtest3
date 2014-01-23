import logging

logger = logging.getLogger(__name__)


class FilterEvents:
    def __init__(self, scraper):
        self.scraper = scraper


    def run(self, parsed_events, filters):
        """
        @param parsed_events: each parsed_event is a dictionary with key ScraperOld.START_TIME, etc.
        @type parsed_events: list of dict
        @type filters: list of dict
        """
        logger.debug("filtering out events ")

        if not filters:
            return parsed_events

        if filters:
            field_name = filters['field_name']
            field_value = filters['field_value']

        return_events = list()
        for idx, parsed_event in enumerate(parsed_events):
            if (parsed_event[field_name]==field_value):
                return_events.append(parsed_event)
            else:
                logger.debug("Skipping event because location does not match: # "+str(idx)+" "+repr(parsed_event))

        return return_events
