import logging
from selenium.common.exceptions import TimeoutException, NoSuchFrameException
from selenium.webdriver.support.wait import WebDriverWait

logger = logging.getLogger(__name__)

class WaitForFrame:
    def __init__(self, scraper):
        self.scraper = scraper

    def run(self, frame_name):
        logger.debug("waiting for browser to load frame: "+frame_name)
        timeoutSeconds = 15

        try:
            WebDriverWait(self.scraper.browser, timeout=timeoutSeconds).until(self.frame_available_cb(frame_name))
        except TimeoutException:
            #could not load element mainFrame within 15 seconds. Just continue without throwing exception...
            logger.warn("could not load frame: "+frame_name+" within "+str(timeoutSeconds)+" seconds")
        else:
            logger.debug("successfully loaded frame: "+frame_name)


    @staticmethod
    def frame_available_cb(frame_reference):
        """Return a callback that checks whether the frame is available."""

        def callback(browser):
            try:
                browser.switch_to_frame(frame_reference)
            except NoSuchFrameException:
                return False
            else:
                return True

        return callback