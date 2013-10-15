from bs4 import BeautifulSoup
import codecs

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchFrameException
from schyoga.models import Studio


class Browser:
    def open(self):
        self.driver = webdriver.Firefox()


    def loadPage(self, url):
        self.driver.get(url)

        #TODO: make "wait timer" more generic - not specific to MindBodyOnline...
        WebDriverWait(self.driver, timeout=10).until(self.frame_available_cb("mainFrame"))
        #driver.switch_to_frame("mainFrame")

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

class Scraper:

    def removeNonVisualTags(self, soup):
        for maxVar in soup.body.find_all(["script", "style"], recursive=True): #"style"
            if maxVar:
                maxVar.decompose()

        strToClean = soup.prettify(formatter="html")
        strToClean = strToClean.replace('&nbsp;', " ")
        strToClean = " ".join(strToClean.split())

        return BeautifulSoup(strToClean)


    def writeToFile(self, soupTag):
        """Write a Tage to a file, even if text has unicode characters

        @param soupTag:
        """
        with codecs.open("C:/tmp/prettyHtml.html", "w", encoding="utf-8") as f:
            f.write(soupTag.prettify(formatter="html"))


    def parseRow(self, headers, schedRow):
        eventData = dict()
        print "Event is: "
        cols = schedRow.select("td")
        print "row has " + str(len(cols)) + " number of columns"

        if len(cols)<=1:
            print str(len(cols))+": Something is up with this row! Text is: "+schedRow.get_text()
            return eventData

        colText = [col.get_text(" ", strip=True) for col in cols]


        for idx,item in enumerate(colText):
            print "huhu"
            print idx
            print item
            if idx<len(headers):
                eventData[headers[idx]] = item

        #eventData[headers[0]] = colText[0]
        #eventData[headers[1]] = colText[1]
        #eventData[headers[2]] = colText[2]
        #eventData[headers[3]] = colText[3]
        #eventData[headers[4]] = colText[4]

        #print eventData

        return eventData

    def run(self):
        print "hello world: start"

        studios = Studio.objects.all().filter(state_name_url='connecticut').order_by('name')
        for studio in studios:
            print studio.name

        exit()

        browser = Browser()
        browser.open()

        #url = "https://clients.mindbodyonline.com/ASP/home.asp?studioid=11999" #"http://google.com"
        url = "http://clients.mindbodyonline.com/ws.asp?studioid=1019"
        pageText = browser.loadPage(url)

        soup = BeautifulSoup(pageText)
        soup = self.removeNonVisualTags(soup)

        mainTable = soup.select("#classSchedule")
        if not mainTable:
            mainTable = "<h1>Did not find Table with ID - #classSchedule</h1>"
            exit(-2)

        if len(mainTable) > 1:
            #TODO: deal with this exceptional scenario
            print "WOW. Why are there more then one table"

        mainTable = mainTable[0]

        headerTable = mainTable.select("#classSchedule-header th")
        #TODO: check that headerTable has exactly one value

        #headers = [ headerID['id'] for headerID in headerTable]
        headers = [ headerTag.string.strip() for headerTag in headerTable]
        print "HEAERS ARE: "
        print headers

        scheduleTable = mainTable.select("#classSchedule-mainTable tr")

        rowNum = 1
        for schedRow in scheduleTable:
            print rowNum
            #dateRow = schedRow.select("td .header")
            dateRow = schedRow.select('td[class="header"]')
            footNotes = schedRow.select('.foot-notes-container')

            controlTag = soup.new_tag("td")

            if dateRow:
                #TODO: test that the len(dateRow) is not larger then 1
                curDate = dateRow[0].get_text()
                curDate = " ".join(curDate.split())
                controlTag.string = curDate
            elif footNotes:
                notes = schedRow.get_text(" ",strip=True)
                controlTag.string = notes
            else:
                eventData = self.parseRow(headers, schedRow)

                if len(eventData) > 3:
                    headerStartTime = 'Start time'
                    headerClasses = 'classes' # "Classes"
                    headerTeacher = 'Teacher'
                    headerDuration = 'Duration'

                    startTime = eventData.get(headerStartTime)
                    className = eventData.get(headerClasses)
                    teacher = eventData.get(headerTeacher)
                    duration = eventData.get(headerDuration)

                    controlTag.string = "maximka - "+str(rowNum)+ ": StartTime: "+startTime+", class: "+className+", teacher: "+teacher+", duration: "+duration

            schedRow.td.insert_before(controlTag)

            rowNum=rowNum+1


        #s = u'\u5E73\u621015'
        self.writeToFile(mainTable)

        browser.loadPage("file:///c:/tmp/prettyHtml.html")

        print 'At the End ---'


if __name__ == "__main__":
    scraper = Scraper()
    scraper.run()
