import logging
from datetime import datetime
from django.core.exceptions import ValidationError
from schyoga.bizobj.parser.scraperOld import ScraperOld
from schyoga.models import Instructor
from dateutil import parser
from schyoga.models.event import Event

logger = logging.getLogger(__name__)


class PrepareEventsForDB:
    def __init__(self, scraper):
        self.scraper = scraper


    def run(self, studio, parsed_events):
        """
        @param parsed_events: each parsed_event is a dictionary with key ScraperOld.START_TIME, etc.
        @type parsed_events: list of dict
        @type studio: Studio
        @type: list of Event
        """
        logger.debug("creating Event objects for saving to DB ")

        db_events = list()

        if not parsed_events:
            logger.warn("No Parsed Events found")
            return

        for idx, parsed_event in enumerate(parsed_events):

            start_time = parsed_event[ScraperOld.START_TIME]
            event_date = parsed_event[ScraperOld.EVENT_DATE]
            dt = parser.parse(event_date + " " + start_time)

            instructor_name_clean = Instructor.clean_up_name(parsed_event[ScraperOld.TEACHER_NAME])

            db_event = Event()
            db_event.start_time = dt
            db_event.comments = parsed_event[ScraperOld.CLASS_NAME]
            db_event.studio = studio
            db_event.instructor_name = instructor_name_clean
            db_event.scrape_uuid = self.scraper.uuid
            db_event.modified_on = datetime.now()
            db_event.created_on = datetime.now()

            try:
                db_event.full_clean()
                db_events.append(db_event)
            except ValidationError as e:
                logger.error("Could not validate event #"+str(idx)+". Message is: "+repr(e.messages) +". Event data is: "+repr(parsed_event))
                db_events.append(None)
                continue

        return db_events

            # use this function to enter into DB Event.objects.get_or_create()
