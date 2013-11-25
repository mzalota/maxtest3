import logging
#from django.core.urlresolvers import reverse
from django.db import models
from django.contrib import admin

#
# Custom field types in here.
#
from django.forms import ModelChoiceField, ModelForm
#from django.utils.html import format_html
#from schyoga.bizobj.page import Page
from schyoga.models.studio import Studio

logger = logging.getLogger(__name__)

#class ManyToManyField_NoSyncdb(models.ManyToManyField):
#    def __init__(self, *args, **kwargs):
#        super(ManyToManyField_NoSyncdb, self).__init__(*args, **kwargs)
#        self.creates_table = False

#alter table schyoga_studio add column address varchar(250) after url_schedule;
#alter table schyoga_studio add column phone varchar(15) after address;
#alter table schyoga_studio add column fb_id varchar(100) after phone;
#alter table schyoga_instructor_content add column source_name varchar(200) default null after content ;
#

class Parsing_History(models.Model):
    studio = models.ForeignKey("Studio")
    #studio_id = models.IntegerField()
    scrape_uuid = models.CharField(max_length=36)
    comment = models.CharField(max_length=100, blank=True, null=True)
    last_crawling = models.DateTimeField(auto_now=True)
    calendar_html = models.TextField(blank=True, null=True)

    class Meta:
        app_label="schyoga"


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

    class Meta:
        app_label="schyoga"

class CustomModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s %s %s" % (obj.id, obj.state_name_url, obj.name)


class MyStudioSiteAdminForm(ModelForm):
    studio = CustomModelChoiceField(queryset=Studio.objects.all().order_by('state_name_url', 'name'))

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

#install facebook API library using (from http://www.pythonforfacebook.com/):
#pip install facebook-sdk


#Getting profile picture of a user  http://stackoverflow.com/questions/2821061/facebook-api-how-do-i-get-a-facebook-users-profile-image-through-the-fb-api
