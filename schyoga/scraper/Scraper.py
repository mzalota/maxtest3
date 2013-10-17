from selenium import webdriver

class Scraper:
    __driver= None

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