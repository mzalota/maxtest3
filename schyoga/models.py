import re
from django.db import models
from django.contrib import admin
# Create your models here.

from datetime import datetime
from time import strftime

#
# Custom field types in here.
#
import django.forms
from django.forms import ModelChoiceField, ModelForm
from django.utils.html import format_html
from picklefield import PickledObjectField
from schyoga.bizobj.state import State


class Instructor(models.Model):
    instructor_name = models.CharField(max_length=150)
    name_url = models.CharField(max_length=150)
    aliases = models.CharField(max_length=1000, blank=True)
    #aliases = PickledObjectField(compress=False, max_length=1000, protocol=0)
    fb_userid = 'JeanneEllenHeaton' #models.CharField(max_length=150, blank=True)
    #body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    modified_on = models.DateTimeField(auto_now=True)
    state = 'new-york'
    #studios = models.ManyToManyField("Studio", blank=True, null=True, db_table="schyoga_instructor_studios")

    class Meta:
        ordering = ('-modified_on',)

    @property
    def aliases_list(self):
        """
        :return:
        """
        return self.aliases.split(";")

    @aliases_list.setter
    def aliases_list(self, value):
        self.aliases = ";".join(value)


    @staticmethod
    def convert_to_url_name(raw_name):
        url_name = raw_name
        url_name = Instructor.clean_up_name(url_name)
        url_name = url_name.replace('-', ' ')
        url_name = " ".join(url_name.split())
        url_name = url_name.lower()
        url_name = url_name.replace(' ', '-')

        return url_name


    @staticmethod
    def clean_up_name(raw_name):
        #remove any apostrophies
        clean_name = raw_name
        clean_name = clean_name.replace("'", '')
        clean_name = clean_name.replace("*", '')  # Sivananda Yoga Centers NY (NYC) has instrucor with name '* *'
        clean_name = clean_name.replace(".", '')
        clean_name = " ".join(clean_name.split())
        #clean_name = re.sub('(\((.*)\))', "", clean_name) # remove anything that appears in brackets ()
        clean_name = re.sub('(\((\d+)\))', "", clean_name) # if number appear inside brackts, remove number and brackets
        clean_name = clean_name.split("@")[0] # remove anything that appears after @ sign
        clean_name = " ".join(clean_name.split())
        clean_name = Instructor.__capitalize(clean_name)

        if clean_name.lower() == 'teacher':
            return ''

        if clean_name.lower() == 'tba':
            return ''

        if clean_name.lower() == 'teacher teacher':
            return ''

        if clean_name.lower().find(' teacher') >= 0: # " Shambhala Yoga & Dance Center
            return ''

        if clean_name.lower() == 'staff' or clean_name.lower() == 'staff staff':
            return ''

        if clean_name.lower().find('staff ') >= 0: #eg "Staff Member"
            return ''

        if clean_name.lower().find(' staff') >= 0: # " GOLDEN BRIDGE STAFF"
            return ''

        if clean_name.lower() == 'yttp': # Yoga to the People-Brooklyn studio has this instructor name
            return ''

        return clean_name


    @staticmethod
    def __capitalize(line):
        if len(line) <= 0:
            return ""
        else:
            return ' '.join([s[0].upper() + s[1:] for s in line.split(' ')])

    @staticmethod
    def find_by_alias(studio_instructors, name):
        instructors_by_alias = dict()
        for instructor in studio_instructors: #studio.instructors.all():
            for alias in instructor.aliases_list:
                if not instructors_by_alias.has_key(alias):
                    instructors_by_alias[alias] = list()
                instructors_by_alias[alias].append(instructor)

        if instructors_by_alias.has_key(name):
            return instructors_by_alias[name]
        else:
            return None


#TODO: introduce State attribute (One-to-Many) to Instructor objects


class InstructorAdmin(admin.ModelAdmin):
    list_display = ('id', 'instructor_name', 'name_url', 'modified_on', 'created_on')


admin.site.register(Instructor, InstructorAdmin)

#class ManyToManyField_NoSyncdb(models.ManyToManyField):
#    def __init__(self, *args, **kwargs):
#        super(ManyToManyField_NoSyncdb, self).__init__(*args, **kwargs)
#        self.creates_table = False


class Studio(models.Model):
    name = models.CharField(max_length=100)
    nameForURL = models.CharField(max_length=100, db_column='name_url')
    state_name_url = models.CharField(max_length=100, db_column='state')
    url_home = models.URLField()
    url_schedule = models.URLField()
    xpath = models.CharField(max_length=1024)
    mindbodyonline_id = models.CharField(max_length=10, blank=True, null=True)
    created_on = models.DateTimeField()
    modified_on = models.DateTimeField()
    fbPageID = 'balancedyoga'   #'balancedyoga'
    instructors = models.ManyToManyField("Instructor", blank=True, null=True, db_table="schyoga_instructor_studios")
    #modified_on = UnixTimestampField(auto_created=True)
    class Meta:
        ordering = ('-modified_on',)


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
    list_display = ('id', 'state_name_url', 'name',  'display_url_home', 'display_url_schedule', 'nameForURL')
    list_display_links = ('id', 'state_name_url', 'name', 'nameForURL')

    def display_url_home(self, obj):
        return format_html('<a href="{0}" target="_blank" title="{0}"><abbr>{1}</abbr></a>', obj.url_home, obj.url_home[:30])

    def display_url_schedule(self, obj):
        return format_html('<a href="{0}" target="_blank" title="{0}"><abbr>{1}</abbr></a>', obj.url_schedule, obj.url_schedule[:20])

    display_url_home.allow_tags = True
    display_url_schedule.allow_tags = True


admin.site.register(Studio, StudioAdmin)


class Event(models.Model):
    instructor_name = models.CharField(max_length=100, blank=True)
    comments = models.CharField(max_length=100,  blank=True, null=True)
    start_time = models.DateTimeField()
    created_on = models.DateTimeField()
    modified_on = models.DateTimeField()
    #modified_on = UnixTimestampField(auto_created=True)
    instructor = models.ForeignKey("Instructor", blank=True, null=True)
    studio = models.ForeignKey("Studio")
    #studio_id
    class Meta:
        ordering = ('-modified_on',)


class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_time', 'instructor_name', 'comments', 'modified_on', 'created_on')


admin.site.register(Event, EventAdmin)
#alter table schyoga_event MODIFY COLUMN instructor_id int(11) default NULL;
#alter table schyoga_event MODIFY COLUMN comments varchar(100) default NULL;

class Parsing_History(models.Model):
    studio = models.ForeignKey("Studio")
    #studio_id = models.IntegerField()
    scrape_uuid = models.CharField(max_length=36)
    comment = models.CharField(max_length=100, blank=True, null=True)
    last_crawling = models.DateTimeField(auto_now=True)
    calendar_html = models.TextField(blank=True, null=True)


class Parsing_HistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'studio_description', 'comment', 'scrape_uuid', 'html_len', 'last_crawling')
    list_editable = list(['comment'])
    list_display_links = ('id', 'studio_description', 'scrape_uuid')
    readonly_fields = ('scrape_uuid', 'last_crawling')

    def studio_description(self, obj):
        return ("%s %s" % (obj.studio.id, obj.studio.name))

    studio_description.short_description = "Studio"

    def html_len(self, obj):
        if obj.calendar_html:
            return ("%s" % len(obj.calendar_html))
        else:
            return "EMPTY"

    html_len.short_description = "HTML Size (bytes)"


admin.site.register(Parsing_History, Parsing_HistoryAdmin)


#alter table schyoga_parsing_history add column scrape_uuid char(36) after studio_id;

# how to render custom form out of json http://stackoverflow.com/questions/9541924/pseudo-form-in-django-admin-that-generates-a-json-object-on-save


class Studio_Site(models.Model):
    studio = models.ForeignKey("Studio")
    config = models.TextField()
    config_crawl = models.TextField()
    config_parse = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    modified_on = models.DateTimeField(auto_now=True)


class CustomModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s %s %s" % (obj.id, obj.state_name_url, obj.name)


class MyStudioSiteAdminForm(ModelForm):
    studio = CustomModelChoiceField(queryset=Studio.objects.all().order_by('state_name_url','name'))

    class Meta:
        model = Studio_Site


class Studio_SiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'studio_description', 'crawl_len', 'parse_len')
    list_display_links = ('id', 'studio_description')
    save_as = True
    save_on_top = True

    form = MyStudioSiteAdminForm

    def studio_description(self, obj):
        return ("%s %s" % (obj.studio.id, obj.studio.name))

    studio_description.short_description = "Studio"

    def crawl_len(self, obj):
        if obj.config_crawl:
            return ("%s" % (len(obj.config_crawl)))
        else:
            return "EMPTY"

    def parse_len(self, obj):
        if obj.config_parse:
            return ("%s" % (len(obj.config_parse)))
        else:
            return "EMPTY"

    crawl_len.short_description = "Config Crawl Size (bytes)"
    parse_len.short_description = "Config Parse Size (bytes)"


    #def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #    if db_field.name == "studio":
    #        kwargs["queryset"] = Studio.objects.filter(owner=request.user)
    #    return super(Studio_SiteAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    #def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #    if db_field.name == "studio":
    #        return CustomContentTypeChoiceField(**kwargs)
    #    return super(Studio_SiteAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Studio_Site, Studio_SiteAdmin)

#alter table schyoga_studio_site ADD COLUMN config_crawl longtext default NULL after config;
#alter table schyoga_studio_site ADD COLUMN config_parse longtext default NULL after config_crawl;



#alter table parsing_history rename to schyoga_parsing_history;
#alter table schyoga_parsing_history MODIFY COLUMN last_crawling datetime;

#alter table schyoga_event MODIFY COLUMN instructor_id int(11) default NULL;

#+---------------+------------+------+-----+-------------------+----------------+
#| Field         | Type       | Null | Key | Default           | Extra          |
#+---------------+------------+------+-----+-------------------+----------------+
#| id            | int(11)    | NO   | PRI | NULL              | auto_increment |
#| studio_id     | int(11)    | YES  |     | NULL              |                |
#| last_crawling | timestamp  | NO   |     | CURRENT_TIMESTAMP |                |
#| calendar_html | mediumtext | YES  |     | NULL              |                |
#+---------------+------------+------+-----+-------------------+----------------+

#| Field           | Type         | Null | Key | Default           | Extra          |
#+-----------------+--------------+------+-----+-------------------+----------------+
#| id              | int(11)      | NO   | PRI | NULL              | auto_increment |
#| studio_id       | int(11)      | YES  |     | NULL              |                |
#| start_time      | datetime     | YES  |     | NULL              |                |
#| instructor_name | varchar(100) | YES  |     | NULL              |                |
#| instructor_id   | int(11)      | YES  |     | NULL              |                |
#| comments        | varchar(100) | YES  |     | NULL              |                |
#| created_on      | datetime     | YES  |     | NULL              |                |
#| modified_on     | timestamp    | NO   |     | CURRENT_TIMESTAMP |                |


# id              | int(11)       | NO   | PRI | NULL              | auto_increment |
# instructor_name | varchar(150)  | NO   |     | NULL              |                |
# name_url        | varchar(150)  | NO   | UNI | NULL              |                |
# aliases         | varchar(1000) | YES  |     | NULL              |                |
# created_on      | datetime      | YES  |     | NULL              |                |
# modified_on     | timestamp     | NO   |     | CURRENT_TIMESTAMP |                |


#app1_studio table
#+-------------------+---------------+------+-----+-------------------+----------------+
#| Field             | Type          | Null | Key | Default           | Extra          |
#+-------------------+---------------+------+-----+-------------------+----------------+
#| id                | int(11)       | NO   | PRI | NULL              | auto_increment |
#| name              | varchar(100)  | YES  |     | NULL              |                |
#| state             | varchar(100)  | YES  |     | NULL              |                |
#| name_url          | varchar(100)  | YES  | UNI | NULL              |                |
#| url_home          | varchar(255)  | YES  |     | NULL              |                |
#| url_schedule      | varchar(1024) | YES  |     | NULL              |                |
#| xpath             | varchar(1024) | YES  |     | NULL              |                |
#| mindbodyonline_id | varchar(10)   | YES  |     | NULL              |                |
#| created_on        | datetime      | YES  |     | NULL              |                |
#| modified_on       | timestamp     | NO   |     | CURRENT_TIMESTAMP |                |
#+-------------------+---------------+------+-----+-------------------+----------------+


#create table schyoga_studio_instructors
#(id int(11) NOT NULL auto_increment, instructor_id int(11) default NULL, studio_id int(11) default NULL, PRIMARY KEY (id))
#ENGINE=InnoDB;

# alter table app1_instructor add column fb_userid varchar(256) after aliases;

#install facebook API library using (from http://www.pythonforfacebook.com/):
#pip install facebook-sdk


#Getting profile picture of a user  http://stackoverflow.com/questions/2821061/facebook-api-how-do-i-get-a-facebook-users-profile-image-through-the-fb-api
