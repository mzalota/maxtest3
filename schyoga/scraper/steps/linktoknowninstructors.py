import logging
import re
from schyoga.models import Instructor

logger = logging.getLogger(__name__)

class LinkToKnownInstructors:

    def __init__(self, scraper):
        self.scraper = scraper


    def run(self, studio_instructors, parsed_instructors):

        logger.debug("Linking parsed instructors to known instructors")

        #parsed_instructors = dict((db_event.instructor_name,) for db_event in db_events)

        studio_instructor_names = dict((instructor.name_url, instructor) for instructor in studio_instructors)
        #logger.debug(" studio_instructor_names var is: "+repr(studio_instructor_names))

        matched = dict()
        unmatched = set()
        for instr_raw, name_url in parsed_instructors.iteritems():
            if studio_instructor_names.has_key(name_url):
                matched[instr_raw] = studio_instructor_names[name_url]
                #parsed_instructors[instr_raw] = studio_instructor_names[name_url]
            else:
                unmatched.add(instr_raw)

        return matched

    #TODO: WORK ON THIS FUNCTION.
    def run2(self, studio, db_events):
        logger.debug("Linking parsed instructors to known instructors")
        unmatched = set()

        if not db_events or len(db_events)<=0:
            logger.warn("No db_events objects found passed ")
            return unmatched

        for db_event in db_events:
            parsed_name = Instructor.clean_up_name(db_event.instructor_name)
            found = Instructor.find_by_alias(studio, parsed_name)
            if found:
                #TODO: Deal with case when more then one Instructor with same alias name is found
                db_event.instructor = found[0]
            else:
                unmatched.add(parsed_name)
            #if studio_instructor_names.has_key(parsed_name_url):
            #    db_event.instructor = studio_instructor_names[parsed_name_url]
            #else:

            #    if unmatched.has_key(parsed_name_url):
            #        db_event.instructor = unmatched[parsed_name_url]
            #    else:
            #        newInstructor = Instructor()
            #        #TODO: Need to have a "Clean Up Instructor Name" function
            #        newInstructor.instructor_name = db_event.instructor_name
            #        #TODO: need to verify uniqueness of the parsed_name_url
            #        newInstructor.instructor_name = parsed_name_url
            #        unmatched[parsed_name_url] = newInstructor

        return unmatched