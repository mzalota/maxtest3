import logging
import codecs
from schyoga.models import Instructor

logger = logging.getLogger(__name__)

class DealWithNewInstructors:

    def __init__(self, scraper):
        self.scraper = scraper


    def run(self, studio, unmatched_instructors, file_path):
        logger.debug("Logging new instructors to file C:/tmp/unknown_instructors.csv")
        formated_list = "" #"studio_id,studio_name,state,instructor_name,instructor_name_for_url"
        for instructor in unmatched_instructors:
            formated_list += "\r\n"
            clean_instructor = Instructor.clean_up_name(instructor)
            if len(clean_instructor) == 0:
                if len(instructor) == 0:
                    logger.warn("Ignoring invalid instructor name: "+instructor)
                continue

            formated_list += str(studio.id)+","+studio.name+","+studio.state_name_url+", "+instructor+", "+Instructor.convert_to_url_name(instructor)

            #logger.debug("Logging to file new instructor: "+instructor)

        self.writeToFile(formated_list, file_path)


    def writeToFile(self, text, file_path):
        """Write a Tag to a file, even if text has unicode characters

        """
        with codecs.open(file_path, "a", encoding="utf-8") as f:
            f.write(text)