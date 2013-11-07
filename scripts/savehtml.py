import logging

from schyoga.bizobj.parser.scraperOld import ScraperOld
from schyoga.models import Studio

logger = logging.getLogger(__name__)
#     logger.error('Found '+studios.count()+' instances of Studio objects for studio_url: '+studio_url_name)


def run():
    #non mindonline:
    #Fresh Yoga Erector Square
    #Balanced Yoga

    #Change website address for Elahi Yoga from http://www.elahiyoga.com/ to http://elahiyoga.com/. Remove Schedule page


    # lower case "classes" header at Atmandan https://clients.mindbodyonline.com/ASP/home.asp?studioid=13547
    #Different headers "Adult Classes" and has tab for "Kid Classes": Bread and Yoga https://clients.mindbodyonline.com/ASP/home.asp?studioid=7450
    #Default tab is not "Classes": Dharma Yoga Center: https://clients.mindbodyonline.com/ASP/home.asp?studioid=3914
    #Kundalini Yoga East has column "	Open Classes" instead of classes. It has other tabs.

    #Check Yoga Collective online - no classes at all
    #!!!! Yoga Sole opens not on "Classes" tab
    #!!!Sivananda Yoga center opens in the Wrong tab
    #OmYoga is no longer there. Replaced by single teacher website - http://cyndilee.com/
    #http://balancedyoga.us/schedule/ instead of http://balancedyoga.us/Schedule.html

    #!!!! check keisha-bolden - its broken
    # Yoga to People does not have teacher name!

    #bikram yoga union square is no longger working, but is replaced by bikram yoga herald square: https://clients.mindbodyonline.com/ASP/home.asp?studioid=31021 http://www.bikramyogaheraldsquare.com/

    logger.debug("starting script: savehtml")

    studios = Studio.objects.all().filter(id=96).order_by('id')

    for studio in studios:

        if "mindbodyonline" not in studio.url_schedule:
            logger.warn('Studio is not a MindBodyOnline: '+studio.name)
            continue

        if studio.nameForURL == 'elahi-yoga':
            logger.debug('skipping studio Elahi Yoga because its only private classes')
            continue

        if studio.nameForURL == 'sankalpah-yoga':
            logger.debug('skipping cloased yoga studio sankalpah-yoga')
            continue

        logger.debug('Processing Studio: '+studio.name)

        scraper = ScraperOld()

        #file_name = "bend-and-bloom-yoga.html"
        #url = "https://clients.mindbodyonline.com/ASP/home.asp?studioid=4186"
        #url = "https://clients.mindbodyonline.com/ASP/home.asp?studioid=8603"

        file_name = str(studio.id)+"_"+studio.nameForURL+".html"
        url = studio.url_schedule

        html = scraper.loadHTML(url)

        file_path = scraper.path_to_resources_dir()+file_name
        #scraper.writeToFile(html, file_path)

    logger.debug('At the End of script: savehtml')

    #Load Site into browser
    #Wait for a certain element to load
    #Validate certain elements are present
    #Click on a tab button
    #Wait for a certain element to load
    #Validate that the tab was switched
    #Option 1: Parse MindBodyOnline from site's schedule:
    #
    #
    #
    #Option 2: Parse MindBodyOnline from MindBodyOnline site
    #  need mapping of columns to values.

    # Parse Events:
    #   define unique key: date+time, parsing source, scan number, studio, instructor,
    #
    # model:
    #   sources
