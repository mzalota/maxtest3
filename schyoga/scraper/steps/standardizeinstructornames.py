
import logging
import re
from schyoga.models import Instructor

logger = logging.getLogger(__name__)

class StandardizeInstructorNames:

    def __init__(self, scraper):
        self.scraper = scraper


    def run(self, instructors_raw):

        logger.debug("Standardizing instructor names")

        matching_instructors = dict()
        for instr in instructors_raw:

            #clean_name = instr
            #clean_name = clean_name.replace('-',' ')
            #clean_name = " ".join(clean_name.split()) #replace any consecutive spaces with single white space
            #clean_name = re.sub('(\((.*)\))',"",clean_name)
            #clean_name = " ".join(clean_name.split()) #replace any consecutive spaces with single white space
            #clean_name = clean_name.lower()
            #clean_name = clean_name.replace(' ','-')

            clean_name = Instructor.convert_to_url_name(instr)
            matching_instructors[instr] = clean_name

        #logger.debug("matching_instructors is: "+repr(matching_instructors))
        #logger.debug("matching VALUES is: "+repr(set(matching_instructors.values())))

        return matching_instructors

