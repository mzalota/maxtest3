#from django.utils.html import format_html
#from django.core.urlresolvers import reverse
#from schyoga.bizobj.page import Page

import datetime
from django.db import models
from schyoga.bizobj.schedule import Schedule
from schyoga.bizobj.state import State
#from schyoga.models.instructor import Instructor


class Studio(models.Model):
    name = models.CharField(max_length=100)
    nameForURL = models.CharField(max_length=100, db_column='name_url')
    state_name_url = models.CharField(max_length=100, db_column='state')
    url_home = models.URLField()
    url_schedule = models.URLField()
    address = models.CharField(max_length=250, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    fb_id = models.CharField(max_length=100, blank=True, null=True)
    site_image_cloudinary_id = models.CharField(max_length=150, blank=True, null=True)
    xpath = models.CharField(max_length=1024)
    mindbodyonline_id = models.CharField(max_length=10, blank=True, null=True)
    created_on = models.DateTimeField()
    modified_on = models.DateTimeField()
    fbPageID = None #'balancedyoga'   #'balancedyoga'
    instructors = models.ManyToManyField("Instructor", blank=True, null=True, db_table="schyoga_instructor_studios")

    class Meta:
        ordering = ('-modified_on',)
        app_label="schyoga"

    @staticmethod
    def autocomplete_search_fields():
        return ("name__icontains",)


    def related_label(self):
        return u"%s (%s)" % (self.name, self.id)


    @property
    def schedule_next_week(self):
        start_date = datetime.datetime.now()
        end_date = start_date + datetime.timedelta(days=7)
        #print "end_date is"
        #print repr(end_date)

        startDateStr = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')

        events = self.event_set.all().order_by('start_time').filter(start_time__gte=startDateStr).filter(start_time__lt=end_date_str)

        return Schedule(events,start_date,7)

    @property
    def state(self):
        """
        :return: State
        """
        return State.createFromUrlName(self.state_name_url)


        # @stateObj.setter
        # def stateObj(self, value):

    #     bla-bla

