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
        logger.debug("Starting to Filtering out events ")

        if not filters:
            return parsed_events

        if filters:
            field_name = filters['field_name']
            expected_value = filters['field_value']

        return_events = list()
        counter = 0
        for idx, parsed_event in enumerate(parsed_events):
            if (parsed_event[field_name]==expected_value):
                return_events.append(parsed_event)
            else:
                counter += 1
                logger.debug("Skipping event #"+str(idx)+", because location it's location "+parsed_event[field_name]+" does not match expected value: "+expected_value)

        if counter > 0:
            logger.info("Filtered out: "+str(counter))

        logger.debug("Finished filtering out events.")

        return return_events