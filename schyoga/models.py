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
    studios = models.ManyToManyField("Studio", blank=True, null=True)

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
        clean_name = " ".join(clean_name.split())
        clean_name = re.sub('(\((.*)\))', "", clean_name) # remove anything that appears in brackets ()
        clean_name = clean_name.split("@")[0] # remove anything that appears after @ sign
        clean_name = " ".join(clean_name.split())
        clean_name = Instructor.__capitalize(clean_name)
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
    instructors = models.ManyToManyField("Instructor", blank=True, null=True)
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
    list_display = (
        'id', 'state_name_url', 'name', 'nameForURL', 'url_home', 'url_schedule', 'modified_on', 'created_on')


admin.site.register(Studio, StudioAdmin)


class Event(models.Model):
    instructor_name = models.CharField(max_length=100, blank=True)
    comments = models.CharField(max_length=100)
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


class Parsing_History(models.Model):
    studio = models.ForeignKey("Studio")
    #studio_id = models.IntegerField()
    scrape_uuid = models.CharField(max_length=36)
    comment = models.CharField(max_length=100, blank=True, null=True)
    last_crawling = models.DateTimeField(auto_now=True)
    calendar_html = models.TextField(blank=True, null=True)


class Parsing_HistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'studio', 'comment', 'scrape_uuid', 'last_crawling')


admin.site.register(Parsing_History, Parsing_HistoryAdmin)


#alter table schyoga_parsing_history add column scrape_uuid char(36) after studio_id;

class Studio_Site(models.Model):
    studio = models.ForeignKey("Studio")
    config = models.TextField()
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
    list_display = ('id', 'studio', 'config')

    form = MyStudioSiteAdminForm

    #def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #    if db_field.name == "studio":
    #        kwargs["queryset"] = Studio.objects.filter(owner=request.user)
    #    return super(Studio_SiteAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    #def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #    if db_field.name == "studio":
    #        return CustomContentTypeChoiceField(**kwargs)
    #    return super(Studio_SiteAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Studio_Site, Studio_SiteAdmin)


#alter table parsing_history rename to schyoga_parsing_history;
#alter table schyoga_parsing_history MODIFY COLUMN last_crawling datetime;



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
