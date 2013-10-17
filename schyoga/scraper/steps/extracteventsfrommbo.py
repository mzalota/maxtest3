import logging
from bs4 import BeautifulSoup
from schyoga.bizobj.parser.scraperOld import ScraperOld

logger = logging.getLogger(__name__)

class ExtractEventsFromMBO:

    def __init__(self, scraper):
        self.scraper = scraper


    def run(self, html_table, headers):
        logger.debug("extracting events from MindBodyOnline page")

        soup = BeautifulSoup(html_table)
        rows = soup.select("tr")

        #headers = list()
        #headers.append("Start time")
        #headers.append(" ")
        #headers.append("Classes")
        #headers.append("Teacher")
        #headers.append("Duration")

        events = []
        rowNum = 1
        for schedRow in rows:
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
                    #startTime = eventData.get(expected_headers[ScraperOld.START_TIME])
                    #className = eventData.get(expected_headers[ScraperOld.CLASS_NAME])
                    #teacher = eventData.get(expected_headers[ScraperOld.TEACHER_NAME])
                    #duration = eventData.get(expected_headers[ScraperOld.DURATION])

                    startTime = eventData.get(ScraperOld.START_TIME)
                    className = eventData.get(ScraperOld.CLASS_NAME)
                    teacher = eventData.get(ScraperOld.TEACHER_NAME)
                    duration = eventData.get(ScraperOld.DURATION)


                    control_msg = "maximka - "+str(rowNum)+ ": StartTime: "+startTime+", class: "+className+", teacher: "+teacher+", duration: "+duration
                    #controlTag.string = control_msg

                    if teacher == "Cancelled Today":
                        continue


                    eventData[ScraperOld.EVENT_DATE] = curDate
                    events.append(eventData)

            #schedRow.td.insert_before(controlTag)

            rowNum=rowNum+1

        logger.debug("found "+str(len(events))+" events")
        return events


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

        if len(colText) > len(headers):
            logger.warn("Encountered more columns: "+str(len(colText))+". Expected columns: "+str(len(headers)) )

        for idx,item in enumerate(colText):
            #logTxt = "Parsing row with an event: "+str(idx)+": column: "+item
            #logger.debug(logTxt)
            if idx<len(headers):
                eventData[headers[idx]] = item
            else:
                break

        return eventData
