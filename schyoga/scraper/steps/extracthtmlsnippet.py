import logging
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class ExtractHtmlSnippet:

    def __init__(self, scraper):
        self.scraper = scraper

    def run(self, html_str, element_id):
        logger.debug("extracting from Html element: "+element_id)
        soup = BeautifulSoup(html_str)
        soup = self.removeNonVisualTags(soup)

        tags = soup.select(element_id)
        if not tags:
            logger.error("Did not find element "+element_id+" in html of length: "+str(len(html_str)))
            return None

        if len(tags) > 1:
            logger.warn("Found more then one element "+element_id+" in html of length: "+str(len(html_str)))

        return tags[0].prettify(formatter="html")

    def removeNonVisualTags(self, soup):
        for maxVar in soup.find_all(["script", "style"], recursive=True): #"style"
            if maxVar:
                maxVar.decompose()

        strToClean = soup.prettify(formatter="html")
        strToClean = strToClean.replace('&nbsp;', " ")
        strToClean = " ".join(strToClean.split())

        return BeautifulSoup(strToClean)