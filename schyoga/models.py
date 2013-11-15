import re
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib import admin

#
# Custom field types in here.
#
from django.forms import ModelChoiceField, ModelForm
from django.utils.html import format_html
from schyoga.bizobj.page import Page
from schyoga.bizobj.state import State

#alter table schyoga_instructor add column state_name_url varchar(100) not null after aliases
#update schyoga_instructor set state_name_url = 'new-york';
#update schyoga_instructor set state_name_url = 'connecticut' where id >= 654 and id <=665;

#select * from schyoga_instructor i join schyoga_instructor_studios ist on i.id=ist.instructor_id where ist.studio_id in (1,2,103,104,105,106);

#select name_url, count(*) as cnt from schyoga_instructor group by name_url having cnt > 1

#alter table schyoga_instructor add column fb_id varchar(150) after phone;
#alter table schyoga_studio add column site_image_cloudinary_id varchar(150) after fb_id;
#alter table schyoga_instructor modify column fb_id varchar(150);

class Instructor(models.Model):
    instructor_name = models.CharField(max_length=150)
    name_url = models.CharField(max_length=150)
    aliases = models.CharField(max_length=1000, blank=True)
    #aliases = PickledObjectField(compress=False, max_length=1000, protocol=0)
    state_name_url = models.CharField(max_length=100) #'new-york'
    fb_id = models.CharField(max_length=150, blank=True) #'JeanneEllenHeaton' #models.CharField(max_length=150, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    modified_on = models.DateTimeField(auto_now=True)
    studios = models.ManyToManyField("Studio", blank=True, null=True, db_table="schyoga_instructor_studios")

    #state = 'connecticut' #'new-york'

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


class InstructorAdmin(admin.ModelAdmin):
    list_per_page = 250

    list_display = ('id', 'state_name_url', 'instructor_name', 'link_to_schedyoga_site', 'studios_cnt', 'fb')
    list_display_links = ('id', 'instructor_name')
    #list_select_related = ['studio']

    def fb(self, obj):
        """
        @type obj: Instructor
        """
        fb_id = obj.fb_id
        if not fb_id:
            return "none"

        #/picture?width=20&height=20
        return format_html('<a href="http://facebook.com/{0}"></a><img src="http://graph.facebook.com/{0}/picture?width=20&height=20"/></a>',fb_id)
        #return format_html('<a href="http://facebook.com/{0}"></a><img src="http://graph.facebook.com/{0}/picture?type=square"/></a>',fb_id)

    def studios_cnt(self, obj):
        """
        @type obj: Instructor
        """
        studio_count = obj.studio_set.count()

        url = reverse('admin:%s_%s_changelist' %("schyoga",  "studio"))
        url = url+"?instructor="+str(obj.id)

        return format_html('<a href="{0}" target="_blank" title="{0}"><span class="glyphicon glyphicon-star"></span>{1}</a>',url,studio_count)

    def link_to_schedyoga_site(self, obj):
        """
        @type obj: Instructor
        """
        evnt_cnt = obj.event_set.count()

        page = Page.createFromEnum(Page.ENUM_TEACHER_PROFILE)
        url = page.urlForTeacherPage(obj)
        return format_html('<a href="{0}" target="_blank" title="{0}"><span class="glyphicon glyphicon-eye-open"></span> {1}</a>', url,evnt_cnt)


    studios_cnt.allow_tags = True
    studios_cnt.short_description = 'Studios'
    link_to_schedyoga_site.allow_tags = True
    link_to_schedyoga_site.short_description = 'SchYoga'
    fb.allow_tags=True
    fb.short_description = "FB"


admin.site.register(Instructor, InstructorAdmin)

#class ManyToManyField_NoSyncdb(models.ManyToManyField):
#    def __init__(self, *args, **kwargs):
#        super(ManyToManyField_NoSyncdb, self).__init__(*args, **kwargs)
#        self.creates_table = False

#alter table schyoga_studio add column address varchar(250) after url_schedule;
#alter table schyoga_studio add column phone varchar(15) after address;
#alter table schyoga_studio add column fb_id varchar(100) after phone;
#alter table schyoga_studio add column site_image_cloudinary_id varchar(150) after fb_id;
#

class Studio(models.Model):
    name = models.CharField(max_length=100)
    nameForURL = models.CharField(max_length=100, db_column='name_url')
    state_name_url = models.CharField(max_length=100, db_column='state')
    url_home = models.URLField()
    url_schedule = models.URLField()
    address = models.CharField(max_length=250, blank=True, null=True,)
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

    list_display = ('id', 'state_name_url', 'name', 'instr', 'site_conf', 'home_url', 'sched_url', 'events', 'pars_hist')
    list_display_links = ('id', 'state_name_url', 'name')
    list_filter = ['state_name_url']

    #http://127.0.0.1:8000/admin/schyoga/studio/?state_name_url__in=connecticut%2Cmassachusetts

    def instr(self, obj):
        """
        @type obj: Studio
        """
        instr_count = obj.instructor_set.count()

        url = reverse('admin:%s_%s_changelist' %("schyoga",  "instructor"))
        url = url+"?studio="+str(obj.id)
        return format_html('<a href="{0}" target="_blank" title="{0}"><span class="glyphicon glyphicon-user"></span>{1}</a>',url,instr_count)

    def pars_hist(self, obj):
        """
        @type obj: Studio
        """
        #http://127.0.0.1:8000/admin/schyoga/parsing_history/?studio=103
        pars_hist_count = obj.parsing_history_set.count()
        #url = reverse('admin:schyoga_parsing_history_list') #,  args=[studio=studio_site_obj.id] )

        url = reverse('admin:%s_%s_changelist' %("schyoga",  "parsing_history"))
        url = url+"?studio="+str(obj.id)
        return format_html('<a href="{0}" target="_blank" title="{0}"><span class="glyphicon glyphicon-flash"></span>{1}</a>',url,pars_hist_count)


    def site_conf(self, obj):
        """
        @type obj: Studio
        """
        studio_site_objs = obj.studio_site_set.all()
        if not studio_site_objs or len(studio_site_objs)<1:
            return ""

        studio_site_obj = studio_site_objs[0]
        url = reverse('admin:%s_%s_change' %(studio_site_obj._meta.app_label,  studio_site_obj._meta.module_name),  args=[studio_site_obj.id] )
        return format_html('<a href="{0}" target="_blank" title="{0}"><span class="glyphicon glyphicon-flash"></span> </a>',url)

    def home_url(self, obj):
        """
        @type obj: Studio
        """
        return format_html('<a href="{0}" target="_blank" title="{0}"><span class="glyphicon glyphicon-home"></span> </a>', obj.url_home)
        #return format_html('<a href="{0}" target="_blank" title="{0}"><abbr>{1}</abbr></a>', obj.url_home, obj.url_home[:30])

    def sched_url(self, obj):
        """
        @type obj: Studio
        """
        mb_flag = ''
        if "mindbodyonline" in obj.url_schedule:
            mb_flag = 'MBO'
        return format_html('<a href="{0}" target="_blank" title="{0}"><span class="glyphicon glyphicon-calendar"></span> {1}</a>', obj.url_schedule, mb_flag)

    def events(self, obj):
        """
        @type obj: Studio
        """
        instr_count = obj.event_set.count()

        page = Page.createFromEnum(Page.ENUM_STUDIO_PROFILE)
        url = page.urlForStudioPage(obj)
        return format_html('<a href="{0}" target="_blank" title="{0}"><span class="glyphicon glyphicon-eye-open"></span> {1}</a>', url,instr_count)


    instr.allow_tags = True
    pars_hist.allow_tags = True
    site_conf.allow_tags = True
    home_url.allow_tags = True
    sched_url.allow_tags = True
    events.allow_tags = True


admin.site.register(Studio, StudioAdmin)


class Event(models.Model):
    instructor_name = models.CharField(max_length=100, blank=True)
    comments = models.CharField(max_length=100,  blank=True, null=True)
    start_time = models.DateTimeField()
    instructor = models.ForeignKey("Instructor", blank=True, null=True)
    studio = models.ForeignKey("Studio")
    scrape_uuid = models.CharField(max_length=36, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    modified_on = models.DateTimeField(auto_now_add=True)

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

#install facebook API library using (from http://www.pythonforfacebook.com/):
#pip install facebook-sdk


#Getting profile picture of a user  http://stackoverflow.com/questions/2821061/facebook-api-how-do-i-get-a-facebook-users-profile-image-through-the-fb-api
