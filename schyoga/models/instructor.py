import logging
import re
import datetime
from django.db import models

from schyoga.bizobj.schedule import Schedule

logger = logging.getLogger(__name__)


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
    name_url = models.CharField(max_length=150, unique=True)
    aliases = models.CharField(max_length=1000, blank=True)
    #aliases = PickledObjectField(compress=False, max_length=1000, protocol=0)
    state_name_url = models.CharField(max_length=100) #'new-york'
    fb_id = models.CharField(max_length=150,
                             blank=True) #'JeanneEllenHeaton' #models.CharField(max_length=150, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    modified_on = models.DateTimeField(auto_now=True)
    studios = models.ManyToManyField("Studio", blank=True, null=True, db_table="schyoga_instructor_studios")

    #state = 'connecticut' #'new-york'

    class Meta:
        ordering = ('instructor_name',)
        app_label="schyoga"


    @staticmethod
    def autocomplete_search_fields():
        return ("instructor_name__icontains","aliases__icontains")


    def related_label(self):
        return u"%s (%s)" % (self.instructor_name, self.id)


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
    def aliases_list(self):
        """
        :return:
        """
        return self.aliases.split(";")

    @property
    def content(self):
        #content_count = self.instructor_content_set.count()
        content_set = self.instructor_content_set.all()
        result = []
        for content_item in content_set:
            if content_item.category == 'studio-site':
                result.append(content_item)

        return result


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

        if clean_name.lower() == 'to be determined':
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