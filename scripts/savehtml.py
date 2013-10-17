import logging

from schyoga.bizobj.parser.scraperOld import ScraperOld
from schyoga.models import Studio

logger = logging.getLogger(__name__)
#     logger.error('Found '+studios.count()+' instances of Studio objects for studio_url: '+studio_url_name)


def run():
    #non mindonline:
    #Fresh Yoga Erector Square
    #Balanced Yoga

    #Studio+Assistant: Baptiste: https://clients.mindbodyonline.com/ASP/home.asp?studioid=1466
    #Location; absolute yoga https://clients.mindbodyonline.com/ASP/home.asp?studioid=13547
    # lower case "classes" header at Atmandan https://clients.mindbodyonline.com/ASP/home.asp?studioid=13547
    #Bikram Yoga online : studio deactivated message https://clients.mindbodyonline.com/ASP/home.asp?studioid=6218
    #Williamsburg Yoga no classes on the schedule: https://clients.mindbodyonline.com/ASP/home.asp?studioid=6433
    #Different headers "Adult Classes" and has tab for "Kid Classes": Bread and Yoga https://clients.mindbodyonline.com/ASP/home.asp?studioid=7450
    #Default tab is not "Classes": Dharma Yoga Center: https://clients.mindbodyonline.com/ASP/home.asp?studioid=3914
    #Location Column: Earth Yoga Online: https://clients.mindbodyonline.com/ASP/home.asp?studioid=7399
    #Location Column: Ishta Yoga
    #Jaya Yoga (Studio columne)
    #Location Ijengar institute of NY
    #Kundalini Yoga East has column "	Open Classes" instead of classes. It has other tabs.
    #Loughing Lotus has columne "	Daily Classes"
    #Some studio on M or N has Instructor instead of Teacher column
    #Pure Yoga has Location and Room!!
    #sankalpah-yoga is kaput
    #Sonic Yoga has instructors
    #TODO: Keep track of Assistants. They soon will become teachers (or may be teachig elsewhere). co-Teacher. Assistant2, Acompanist, etc.
    #The Shala yoga house has pleanty of columns
    #Check Yoga Collective online - no classes at all
    #The Yoga room has "Teacher or Therapist" column and "Acompanist"
    #Yoga sutra is gone yoga sutra nyc
    #!!!! Yoga Sole opens not on "Classes" tab
    #!!!Sivananda Yoga center opens in the Wrong tab
    #OmYoga is no longer there. Replaced by single teacher website - http://cyndilee.com/
    #http://balancedyoga.us/schedule/ instead of http://balancedyoga.us/Schedule.html

    #!!!! check keisha-bolden - its broken
    # Yoga to People does not have teacher name!

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
