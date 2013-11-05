import uuid
from selenium import webdriver

class Scraper:
    __driver= None
    vars = dict()

    def __init__(self):
        self.uuid = uuid.uuid1()

    def run(self):
        pass

    @property
    def browser(self):
        """

        @rtype: webdriver
        """

        if not self.__driver:
            self.__driver = webdriver.Firefox()
            #self.__driver.implicitly_wait(30)

        return self.__driver