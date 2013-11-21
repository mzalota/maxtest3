import codecs
import logging
import schyoga

from bs4 import BeautifulSoup
from schyoga.bizobj.parser.browser import Browser
from schyoga.models import Parsing_History
from schyoga.models.studio import Studio


logger = logging.getLogger(__name__)

#TODO: get rid of this class

class ScraperOld:

    START_TIME = 'start-time'
    CLASS_NAME = 'class-name'
    TEACHER_NAME = 'teacher-name'
    DURATION = 'duration'
    EVENT_DATE = 'date'

    def removeNonVisualTags(self, soup):
        for maxVar in soup.find_all(["script", "style"], recursive=True): #"style"
            if maxVar:
                maxVar.decompose()

        strToClean = soup.prettify(formatter="html")
        strToClean = strToClean.replace('&nbsp;', " ")
        strToClean = " ".join(strToClean.split())

        return BeautifulSoup(strToClean)


    def writeToFile(self, text, file_path):
        """Write a Tage to a file, even if text has unicode characters

        @param soupTag:
        """
        with codecs.open(file_path, "w", encoding="utf-8") as f:
            f.write(text)


    def parseRow(self, headers, schedRow):
        """

        @type headers: list of str
        @type schedRow: SoupTag

        @return:
        @rtype: dict
        """
        eventData = dict()
        cols = schedRow.select("td")

        if len(cols)<=1:
            logTxt = str(len(cols))+": Something is up with this row! Text is: "+schedRow.get_text()
            logger.error(logTxt)
            return eventData

        #parse columns out of the row and for each column value get rid of consecutive white spaces
        colText = [col.get_text(" ", strip=True) for col in cols]

        for idx,item in enumerate(colText):
            logTxt = "Parsing row with an event: "+str(idx)+": column: "+item
            logger.debug(logTxt)
            if idx<len(headers):
                eventData[headers[idx]] = item

        return eventData

    def saveParsingHistory(self, htmlText, studio_id):
        logger.debug("creating new parsing history obj")
        parHist = Parsing_History()
        parHist.calendar_html = htmlText.prettify(formatter="html")
        parHist.studio_id = studio_id
        parHist.save()


    def loadHTML(self, url):
        browser = Browser()
        browser.open()

        pageText = browser.loadPage(url)

        return pageText


    def path_to_resources_dir(self):
        return schyoga.__path__[0] + "\\resources\\"



    def run(self):
        #studios = Studio.objects.all().filter(state_name_url='connecticut').order_by('name')
        #for studio in studios:
        #    print "studioname: "+studio.name

        browser = Browser()
        browser.open()

        #studio = Studio.objects.get(pk=13)

        #url = "https://clients.mindbodyonline.com/ASP/home.asp?studioid=11999" #"http://google.com"
        url = "https://clients.mindbodyonline.com/ASP/home.asp?studioid=8603"
        #url = studio.url_schedule # "http://clients.mindbodyonline.com/ws.asp?studioid=1019"
        pageText = browser.loadPage(url)

        expected_headers = dict()
        expected_headers[ScraperOld.START_TIME] = 'Start time'
        expected_headers[ScraperOld.CLASS_NAME] = 'Classes'
        expected_headers[ScraperOld.TEACHER_NAME] = 'Teacher'
        expected_headers[ScraperOld.DURATION] = 'Duration'

        events = self.parse(pageText, expected_headers)

        #self.saveParsingHistory(self.mainTable, 12)

        #s = u'\u5E73\u621015'
        self.writeToFile(self.mainTable.prettify(formatter="html"), "C:/tmp/prettyHtml.html")

        browser.loadPage("file:///c:/tmp/prettyHtml.html")


    def parse(self, pageText, expected_headers):
        soup = BeautifulSoup(pageText)
        soup = self.removeNonVisualTags(soup)

        events = []
        mainTable = soup.select("#classSchedule")
        if not mainTable:
            logger.error("Did not find Table with ID - #classSchedule. Stoping Parsing")
            return

        if len(mainTable) > 1:

            logger.error("WOW. Why is there more then one table with ID=classSchedule in HTML DOM??. Using the first one.")

        mainTable = mainTable[0]

        headerTable = mainTable.select("#classSchedule-header th")
        #TODO: check that headerTable has exactly one value

        #headers = [ headerID['id'] for headerID in headerTable]
        headers = [ headerTag.string.strip() for headerTag in headerTable]
        logger.info("Parsed Following headers:"+str(headers))

        scheduleTable = mainTable.select("#classSchedule-mainTable tr")

        rowNum = 1
        for schedRow in scheduleTable:
            logger.debug("starting to process schedule row:"+str(rowNum))
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
                    startTime = eventData.get(expected_headers[self.START_TIME])
                    className = eventData.get( expected_headers[self.CLASS_NAME] )
                    teacher = eventData.get(expected_headers[self.TEACHER_NAME])
                    duration = eventData.get(expected_headers[self.DURATION])

                    controlTag.string = "maximka - "+str(rowNum)+ ": StartTime: "+startTime+", class: "+className+", teacher: "+teacher+", duration: "+duration

                    if teacher == "Cancelled Today":
                        continue

                    events.append(eventData)

            schedRow.td.insert_before(controlTag)

            rowNum=rowNum+1

        self.mainTable = mainTable

        return events




