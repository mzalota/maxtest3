from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.html import format_html
from schyoga.models import Instructor
from schyoga.models.event import Event


class EventAdmin(admin.ModelAdmin):
    list_per_page = 100
    list_display = ('id', 'start_time', 'instructor_name', 'instr', 'studio', 'comments','created_on')

    def instr(self, obj):
        """
        @type obj: Event
        """

        instructor_name = obj.instructor_name
        instructor_name_url = Instructor.convert_to_url_name(instructor_name)
        studio_id = obj.studio_id
        state_name_url = obj.studio.state_name_url

        url = reverse('admin:%s_%s_add' % ("schyoga", "instructor"))
        url = url +('?name_url=%s&instructor_name=%s&aliases=%s&state_name_url=%s&studios=%s'% (instructor_name_url,instructor_name,instructor_name,state_name_url,studio_id))

        link_url = reverse('admin:%s_%s_add' % ("schyoga", "instructor"))

        return format_html('<a href="{0}" target="_blank" title="{0}">add</a>', url)

    instr.allow_tags = True


admin.site.register(Event, EventAdmin)