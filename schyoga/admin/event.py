from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.html import format_html
from schyoga.models.instructor import Instructor
from schyoga.models.event import Event
from django.db.models import Q


class EventAdmin(admin.ModelAdmin):
    list_per_page = 100
    list_display = ('id', 'start_time', 'instructor_name', 'instr', 'studio_link', 'comments','created_on')
    change_list_template = "admin/schyoga/event/change_list_filter_sidebar.html"

    def studio_link(self, obj):
        """
        @type obj: Event
        """

        url = reverse('admin:%s_%s_changelist' % ("schyoga", "studio"))
        url = url + "?id=" + str(obj.studio_id)
        return format_html('<a href="{0}" target="_blank" title="{0}"><span class="glyphicon glyphicon-star"></span>{1}</a>', url, obj.studio.name)


    def instr(self, obj):
        """
        @type obj: Event
        """

        if obj.instructor:
            url = reverse('admin:%s_%s_changelist' % ("schyoga", "instructor"))
            url = url + "?id=" + str(obj.instructor_id)
            return  format_html('<a href="{0}" target="_blank" title="{0}"><span class="glyphicon glyphicon-user"></span></a>', url)

        instructor_name = obj.instructor_name
        if not instructor_name:
            return

        #if instructor_name.strip() == '':
        #    return

        if Instructor.clean_up_name(instructor_name) == '':
            return

        instructor_name_url = Instructor.convert_to_url_name(instructor_name)

        studio_id = obj.studio_id
        state_name_url = obj.studio.state_name_url

        add_url = reverse('admin:%s_%s_add' % ("schyoga", "instructor"))
        add_url = add_url +('?name_url=%s&instructor_name=%s&aliases=%s&state_name_url=%s&studios=%s'% (instructor_name_url,instructor_name,instructor_name,state_name_url,studio_id))
        add_link='<a href="'+add_url+'" target="_blank" title="Add: '+instructor_name+'"><span class="glyphicon glyphicon-floppy-disk"></span> Add New</a>'


        instructor_sub_names = instructor_name.split(" ")
        matching_instructors = Instructor.objects.all().filter(aliases__contains=instructor_name)
        if matching_instructors:
            #link_url = reverse('admin:%s_%s_add' % ("schyoga", "instructor"))
            result = ""
            for instr in matching_instructors:
                url = reverse('admin:%s_%s_change' % ("schyoga", "instructor"), args=[instr.id])
                studio_names = ""
                studios = instr.studio_set.all()
                for studio in studios:
                    studio_names = studio_names+", "+studio.name
                title = instr.instructor_name+ ", id "+str(instr.id)+"; "+studio_names
                result = result +  "<a href='{0}' target='_blank' title='{1}'><span class='glyphicon glyphicon-link'></span> {2}</a><br> ".format(url, title, instr.instructor_name)
            return result+add_link

        query = Q()
        if len(instructor_sub_names) > 1:
            print "count is: "+repr(instructor_sub_names[0])+" "+repr(instructor_sub_names[1])
            query = query | Q(aliases__contains=instructor_sub_names[0])
            query = query | Q(aliases__contains=instructor_sub_names[1])

            matching_instructors = Instructor.objects.all().filter(query)
            if matching_instructors:
                #link_url = reverse('admin:%s_%s_add' % ("schyoga", "instructor"))
                result = ""
                for instr in matching_instructors:
                    studio_names = ""
                    studios = instr.studio_set.all()
                    for studio in studios:
                        studio_names = studio_names+", "+studio.name

                    url = reverse('admin:%s_%s_change' % ("schyoga", "instructor"), args=[instr.id])
                    title = instr.instructor_name+ ", id "+str(instr.id)+"; "+studio_names
                    result = result +  "<a href='{0}' target='_blank' title='{1}'><span class='glyphicon glyphicon-link'></span> {2} </a><br>".format(url, title, instr.instructor_name)
                return result+add_link

        return add_link


    instr.allow_tags = True
    studio_link.allow_tags = True

    studio_link.short_description = "Studio"

admin.site.register(Event, EventAdmin)