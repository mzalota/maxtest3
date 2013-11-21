from django.contrib import admin
from django.db import models


class Event(models.Model):
    instructor_name = models.CharField(max_length=100, blank=True)
    comments = models.CharField(max_length=100, blank=True, null=True)
    start_time = models.DateTimeField()
    instructor = models.ForeignKey("Instructor", blank=True, null=True)
    studio = models.ForeignKey("Studio")
    scrape_uuid = models.CharField(max_length=36, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    modified_on = models.DateTimeField(auto_now_add=True)

    #studio_id
    class Meta:
        ordering = ('-modified_on',)
        app_label="schyoga"


class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_time', 'instructor_name', 'comments', 'modified_on', 'created_on')


admin.site.register(Event, EventAdmin)
#alter table schyoga_event MODIFY COLUMN instructor_id int(11) default NULL;
#alter table schyoga_event MODIFY COLUMN comments varchar(100) default NULL;