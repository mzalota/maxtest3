from django.db import models

__author__ = 'mzalota'


class Instructor_Content(models.Model):
    instructor = models.ForeignKey("Instructor")
    category = models.CharField(max_length=100)
    content = models.TextField()
    source_name = models.CharField(max_length=200, blank=True, null=True)
    source_url = models.URLField(blank=True, null=True)
    scrape_uuid = models.CharField(max_length=36, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        app_label="schyoga"