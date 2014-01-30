import logging
from schyoga.models.studio import Studio
from schyoga.scraper.scraper import Scraper
from schyoga.scraper.steps.crawlmbo import CrawlMBO

import json

logger = logging.getLogger(__name__)

def run():
    logger.debug("starting script: crawl")

    scraper = Scraper()
    studios = Studio.objects.all().filter(id__gte=72).filter(id__lte=72).order_by('id')
    for studio in studios:
        process_studio(scraper, studio)

    logger.debug('At the end of script: crawl')


def process_studio(scraper, studio):
    """

    @type scraper: Scraper
    @type studio: Studio
    """
    logger.debug("STARTING to crawl for studio: "+str(studio.id)+", "+studio.name)

    studio_site_set = studio.studio_site_set.all()
    if not studio_site_set:
        logger.error("Config data is not specified for studio: "+str(studio.id)+", "+studio.name)
        return

    if len(studio_site_set)>1:
        logger.error("More then one Studio_Site object exists for  studio: "+str(studio.id)+", "+studio.name)
        return

    config_crawl_json = studio_site_set[0].config_crawl
    config_crawl = json.loads(config_crawl_json)
    for step in config_crawl:
        if step['step_name'] == 'MBOLReadHtml':
            mbol_studio_id = step['mbol_studio_id']
            click_tab_name = step.get('click_tab_name', None)
            CrawlMBO(scraper).run(studio, mbol_studio_id, None, click_tab_name)
        else:
            logger.error("Unrecognized Crawling step: "+step['step_name'])

    logger.debug("FINISHED crawling for studio: "+str(studio.id)+", "+studio.name)
