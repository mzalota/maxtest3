import logging
from selenium.common.exceptions import TimeoutException, NoSuchFrameException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

logger = logging.getLogger(__name__)



class WaitForElement:

    def __init__(self, scraper):
        self.scraper = scraper

    def run(self, element_name):
        logger.debug("waiting for browser to load element: "+element_name)

        try:
            WebDriverWait(self.scraper.browser, timeout=15).until(self.frame_available_cb("mainFrame"))
            WebDriverWait(self.scraper.browser, timeout=15).until(self.element_available_cb("main-content"))
        except TimeoutException:
            #could not load element mainFrame within 15 seconds. Just continue...
            logger.warn("threw a TimeoutException exception: "+repr(TimeoutException))
            pass

        #try:
        #    # we have to wait for the page to refresh, the last thing that seems to be updated is the title
        #    WebDriverWait(self.scraper.browser, timeout=15).until(EC.presence_of_element_located((By.ID , "main-content"))) #self.scraper.browser.find_element(
        #
        #except TimeoutException:
        #    #could not load element mainFrame within 15 seconds. Just continue...
        #    logger.warn("threw a TimeoutException exception ")

        logger.debug("Finished waiting for browser to load element: "+element_name)

    def element_available_cb(self, element_id):
        """Return a callback that checks whether the frame is available."""

        def callback(browser):
            try:
                logger.warn("trying to switch to element: "+element_id)
                browser.find_element_by_id(element_id)
            except Exception as e:
            #except NoSuchFrameException:
                logger.warn("Got Exception: "+repr(e))
                return False
            else:
                logger.warn("Successfully switched to element : "+element_id)
                return True

        return callback


    def frame_available_cb(self, frame_reference):
        """Return a callback that checks whether the frame is available."""

        def callback(browser):
            try:
                logger.warn("trying to switch to frame: "+frame_reference)
                browser.switch_to_frame(frame_reference)
            except NoSuchFrameException:
                logger.warn("Got Exception NoSuchFrameException ")
                return False
            else:
                logger.warn("Successfully switched to frame : "+frame_reference)
                return True

        return callback