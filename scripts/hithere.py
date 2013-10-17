import logging

from schyoga.bizobj.parser.scraperOld import ScraperOld

logger = logging.getLogger(__name__)
#     logger.error('Found '+studios.count()+' instances of Studio objects for studio_url: '+studio_url_name)


def run():

    logger.debug("starting scraper script")

    scraper = ScraperOld()
    scraper.run()

    logger.debug('At the End of scraper script')