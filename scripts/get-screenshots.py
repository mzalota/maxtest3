import logging
import json
#from cloudinary import cloudinary
from schyoga.models import Studio
from schyoga.scraper.scraper import Scraper
from schyoga.scraper.steps.loadurl import LoadUrl

import cloudinary
import cloudinary.uploader
import cloudinary.api

logger = logging.getLogger(__name__)

def run():

    logger.debug("starting script: get-screenshots")

    scraper = Scraper()
    studios = Studio.objects.all().filter(id__gte=70).filter(id__lte=200).order_by('id')
    for studio in studios:
        process_studio(scraper, studio)

    logger.debug('At the end of script: get-screenshots')



def process_studio(scraper, studio):
    logger.debug("processing studio: "+str(studio.id)+", "+studio.name)

    #http://cloudinary.com/documentation/django_integration#getting_started_guide

    url = studio.url_home
    filename = "C:\\tmp\\new\\screenshots\\"+studio.nameForURL+".png"
    logger.debug("saving screenshot of site: "+url+" to file: "+filename)

    LoadUrl(scraper).run(url)
    scraper.browser.maximize_window()
    scraper.browser.get_screenshot_as_file(filename)

    cloudinary.config(
        cloud_name = "scheduleyoga",
        api_key = "184789393887359",
        api_secret = "5b_y47V0o2CSKgHWDLKyxf4Nmto"
    )

    image_public_id = 'site-screenshots/'+studio.nameForURL
    result = cloudinary.uploader.upload(filename, public_id = image_public_id)
    logger.debug("result of uploading to Cloundary: "+repr(result))

    studio.site_image_cloudinary_id = result['public_id']+".png"
    studio.save()

    #WaitForFrame(scraper).run(frame_name=step['frame_name'])

    #driver.get("C:\Documents and Settings\mzalota\Desktop\TOGAF\keyfile.txt")
    #driver.get("C:/tmp/prettyHtml.html")
