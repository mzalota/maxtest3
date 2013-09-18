from django.db import models
from django.contrib import admin
# Create your models here.

from datetime import datetime
from time import strftime

#
# Custom field types in here.
#
class UnixTimestampField(models.DateTimeField):
    """UnixTimestampField: creates a DateTimeField that is represented on the
    database as a TIMESTAMP field rather than the usual DATETIME field.
    """
    def __init__(self, null=False, blank=False, **kwargs):
        super(UnixTimestampField, self).__init__(**kwargs)
        # default for TIMESTAMP is NOT NULL unlike most fields, so we have to
        # cheat a little:
        self.blank, self.isnull = blank, null
        self.null = True # To prevent the framework from shoving in "not null".

    def db_type(self):
        typ=['TIMESTAMP']
        # See above!
        if self.isnull:
            typ += ['NULL']
        if self.auto_created:
            typ += ['default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP']
        return ' '.join(typ)

    def to_python(self, value):
        return value
        #return datetime.fromtimestamp(value, None)
        # datetime.from_timestamp(value)

    def get_db_prep_value(self, value, connection, prepared=False):
        if value==None:
            return None
        return strftime('%Y%m%d%H%M%S',value.timetuple())


class Instructor(models.Model):
    instructor_name = models.CharField(max_length=150)
    name_url = models.CharField(max_length=150)
    aliases = models.CharField(max_length=1000,blank=True)
    fb_userid = models.CharField(max_length=150, blank=True)
    #body = models.TextField()
    created_on = models.DateTimeField(blank=True)
    modified_on = models.DateTimeField()
    #modified_on = UnixTimestampField(auto_created=True)
    class Meta:
        ordering = ('-modified_on',)

class InstructorAdmin(admin.ModelAdmin):
    list_display = ('id', 'instructor_name', 'name_url', 'modified_on', 'created_on')


admin.site.register(Instructor, InstructorAdmin)


class Studio(models.Model):
    name = models.CharField(max_length=100)
    name_url = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    url_home = models.URLField()
    url_schedule = models.URLField()
    xpath = models.CharField(max_length=1024)
    mindbodyonline_id = models.CharField(max_length=10)
    created_on = models.DateTimeField()
    modified_on = models.DateTimeField()
    #modified_on = UnixTimestampField(auto_created=True)
    class Meta:
        ordering = ('-modified_on',)


class StudioAdmin(admin.ModelAdmin):
    list_display = ('id', 'state', 'name', 'name_url', 'url_home', 'url_schedule', 'modified_on', 'created_on')


admin.site.register(Studio, StudioAdmin)


class Event(models.Model):
    instructor_name = models.CharField(max_length=100)
    comments = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    created_on = models.DateTimeField()
    modified_on = models.DateTimeField()
    #modified_on = UnixTimestampField(auto_created=True)
    instructor = models.ForeignKey("Instructor")
    studio = models.ForeignKey("Studio")
    #studio_id
    class Meta:
        ordering = ('-modified_on',)


class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_time', 'instructor_name', 'comments', 'modified_on', 'created_on')


admin.site.register(Event, EventAdmin)


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


# alter table app1_instructor add column fb_userid varchar(256) after aliases;

#install facebook API library using (from http://www.pythonforfacebook.com/):
#pip install facebook-sdk


#Getting profile picture of a user  http://stackoverflow.com/questions/2821061/facebook-api-how-do-i-get-a-facebook-users-profile-image-through-the-fb-api