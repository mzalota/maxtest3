from django.utils.html import format_html
from django.core.urlresolvers import reverse
from schyoga.bizobj.page import Page

import datetime
from django.db import models
from schyoga.bizobj.schedule import Schedule
from schyoga.bizobj.state import State

from django.contrib import admin


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

class StudioAdmin(admin.ModelAdmin):
    list_per_page = 250

    list_display = (
        'id', 'state_name_url', 'name', 'instr', 'site_conf', 'home_url', 'sched_url', 'events', 'pars_hist')
    list_display_links = ('id', 'state_name_url', 'name')
    list_filter = ['state_name_url']

    #http://127.0.0.1:8000/admin/schyoga/studio/?state_name_url__in=connecticut%2Cmassachusetts

    def instr(self, obj):
        """
        @type obj: schyoga.models.studio.Studio
        """
        instr_count = obj.instructor_set.count()

        url = reverse('admin:%s_%s_changelist' % ("schyoga", "instructor"))
        url = url + "?studio=" + str(obj.id)
        return format_html(
            '<a href="{0}" target="_blank" title="{0}"><span class="glyphicon glyphicon-user"></span>{1}</a>', url,
            instr_count)

    def pars_hist(self, obj):
        """
        @type obj: schyoga.models.studio.Studio
        """
        #http://127.0.0.1:8000/admin/schyoga/parsing_history/?studio=103
        pars_hist_count = obj.parsing_history_set.count()
        #url = reverse('admin:schyoga_parsing_history_list') #,  args=[studio=studio_site_obj.id] )

        url = reverse('admin:%s_%s_changelist' % ("schyoga", "parsing_history"))
        url = url + "?studio=" + str(obj.id)
        return format_html(
            '<a href="{0}" target="_blank" title="{0}"><span class="glyphicon glyphicon-flash"></span>{1}</a>', url,
            pars_hist_count)


    def site_conf(self, obj):
        """
        @type obj: schyoga.models.studio.Studio
        """
        studio_site_objs = obj.studio_site_set.all()
        if not studio_site_objs or len(studio_site_objs) < 1:
            return ""

        studio_site_obj = studio_site_objs[0]
        url = reverse('admin:%s_%s_change' % (studio_site_obj._meta.app_label, studio_site_obj._meta.module_name),
                      args=[studio_site_obj.id])
        return format_html(
            '<a href="{0}" target="_blank" title="{0}"><span class="glyphicon glyphicon-flash"></span> </a>', url)

    def home_url(self, obj):
        """
        @type obj: schyoga.models.studio.Studio
        """
        return format_html(
            '<a href="{0}" target="_blank" title="{0}"><span class="glyphicon glyphicon-home"></span> </a>',
            obj.url_home)
        #return format_html('<a href="{0}" target="_blank" title="{0}"><abbr>{1}</abbr></a>', obj.url_home, obj.url_home[:30])

    def sched_url(self, obj):
        """
        @type obj: schyoga.models.studio.Studio
        """
        mb_flag = ''
        if "mindbodyonline" in obj.url_schedule:
            mb_flag = 'MBO'
        return format_html(
            '<a href="{0}" target="_blank" title="{0}"><span class="glyphicon glyphicon-calendar"></span> {1}</a>',
            obj.url_schedule, mb_flag)

    def events(self, obj):
        """
        @type obj: schyoga.models.studio.Studio
        """
        instr_count = obj.event_set.count()

        page = Page.createFromEnum(Page.ENUM_STUDIO_PROFILE)
        url = page.urlForStudioPage(obj)
        return format_html(
            '<a href="{0}" target="_blank" title="{0}"><span class="glyphicon glyphicon-eye-open"></span> {1}</a>', url,
            instr_count)


    instr.allow_tags = True
    pars_hist.allow_tags = True
    site_conf.allow_tags = True
    home_url.allow_tags = True
    sched_url.allow_tags = True
    events.allow_tags = True




admin.site.register(Studio, StudioAdmin)