import logging
from selenium import webdriver
from selenium.common.exceptions import NoSuchFrameException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

logger = logging.getLogger(__name__)


class Browser:
    def open(self):
        self.driver = webdriver.Firefox()


    def loadPage(self, url, schedule_tab_text):

        self.driver.implicitly_wait(10)
        self.driver.get(url)

        #TODO: make "wait timer" more generic - not specific to MindBodyOnline...
        try:
            WebDriverWait(self.driver, timeout=15).until(self.frame_available_cb("mainFrame"))
        except TimeoutException:
            #could not load element mainFrame within 15 seconds. Just continue...
            pass
        #driver.switch_to_frame("mainFrame")

        scheduleTabText = 'CLASSES' #NYC CLASSES

        if schedule_tab_text:
            logger.info('Clicking on Tab button: '+scheduleTabText)
            self.driver.find_element_by_link_text(scheduleTabText).click()

            try:
                WebDriverWait(self.driver, timeout=15).until(self.frame_available_cb("mainFrame"))
            except TimeoutException:
                #could not load element mainFrame within 15 seconds. Just continue...
                pass

        #logger.info('Clicking on Next Week button')
        #self.driver.find_element_by_id("week-arrow-r").click()

        pageText = self.driver.page_source

        return pageText

    def getScreenshot(self):
        #TODO: figure out how to take a screenshot of the website.
        #driver.get_screenshot_as_png()
        #driver.save_screenshot

        #driver.get("C:\Documents and Settings\mzalota\Desktop\TOGAF\keyfile.txt")
        #driver.get("C:/tmp/prettyHtml.html")
        pass


    def close(self):
        self.driver.close()


    def frame_available_cb(self, frame_reference):
        """Return a callback that checks whether the frame is available."""

        def callback(browser):
            try:
                browser.switch_to_frame(frame_reference)
            except NoSuchFrameException:
                return False
            else:
                return True

        return callback