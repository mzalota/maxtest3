import re
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.html import format_html
from schyoga.models.instructor import Instructor
from schyoga.models.event import Event
from django.db.models import Q
from django.contrib import messages


class EventAdmin(admin.ModelAdmin):
    list_per_page = 100
    list_display = ('id', 'start_time', 'instructor_name', 'instr', 'studio_link', 'comments','created_on')
    change_list_template = "admin/schyoga/event/change_list_filter_sidebar.html"
    save_as = True
    save_on_top = True
    actions = ['link_to_instructor']

    class Media:
        js = ('js/admin/event.js',)


    def link_to_instructor(self, request, queryset):
        """

        @type request: django.http.HttpRequest
        @type queryset: list of Event
        """

        assert queryset
        assert request
        assert request.POST

        print "request is: "+repr(request)

        if not request.POST.has_key('instructor_id'):
            messages.error(request, 'Please do not use this action!')
            return

        instructor_id = request.POST['instructor_id']
        instructor = Instructor.objects.get(id=instructor_id)
        if not instructor:
            messages.error(request, 'Could not find instructor object with id '+str(instructor_id))
            return

        for event in queryset:
            print "instructor id is: "+instructor_id
            print "instructor name is: "+event.instructor_name
            print "event id is: "+str(event.id)
            instructor.link_to_event(event)

            events = Event.objects.filter(instructor_name=event.instructor_name, studio=event.studio, instructor=None)
            events_count = events.count()
            events.update(instructor=instructor)


            messages.info(request, 'updated instructor '+instructor.instructor_name+' based  on event with id '+str(event.id)+"; Updated "+str(events_count)+" events with instructor")


    def studio_link(self, obj):
        """
        @type obj: Event
        """

        url = reverse('admin:%s_%s_changelist' % ("schyoga", "studio"))
        url = url + "?id=" + str(obj.studio_id)
        return format_html('<a href="{0}" target="_blank" title="{0}"><span class="glyphicon glyphicon-star"></span>{1}</a>', url, obj.studio.name)


    def __build_html_link_to_instructor(self, instr, event):

        url = reverse('admin:%s_%s_change' % ("schyoga", "instructor"), args=[instr.id])

        studio_names = ""
        studios = instr.studio_set.all()
        for studio in studios:
            if studio_names == '':
                studio_names = studio.name
            else:
                studio_names = studio.name + ", " + studio_names

        title = instr.instructor_name + "; id " + str(instr.id) + "; " + studio_names

        str_html = ""
        str_html = str_html + '<div style="display:none;"> <input name="instructor_id" type="checkbox" value="' + str(
            instr.id) + '" title="' + instr.instructor_name + '"> </div>'
        str_html = str_html + "<a href='#' class='maxtest' title='Link instructor {0} to studio {1}'><strong><span class='glyphicon glyphicon-link large'></span>-Link To</strong></a> ".format(
            instr.instructor_name, event.studio.name)
        str_html = str_html + "<a href='{0}' target='_blank' title='{1}'> {2}</a> ".format(url, title, instr.aliases)
        str_html = str_html + "<br>"

        return str_html

    def instr(self, event):
        """
        @type event: Event
        """

        if event.instructor:
            url = reverse('admin:%s_%s_changelist' % ("schyoga", "instructor"))
            url = url + "?id=" + str(event.instructor_id)
            return  format_html('<a href="{0}" target="_blank" title="{0}"><span class="glyphicon glyphicon-user"></span></a>', url)

        instructor_name = event.instructor_name
        if not instructor_name:
            return

        if Instructor.clean_up_name(instructor_name) == '':
            return

        instructor_name_url = Instructor.convert_to_url_name(instructor_name)

        studio_id = event.studio_id
        state_name_url = event.studio.state_name_url

        add_url = reverse('admin:%s_%s_add' % ("schyoga", "instructor"))
        add_url = add_url +('?name_url=%s&instructor_name=%s&aliases=%s&state_name_url=%s&studios=%s'% (instructor_name_url,instructor_name,instructor_name,state_name_url,studio_id))
        add_link='<a href="'+add_url+'" target="_blank" title="Add: '+instructor_name+'"><span class="glyphicon glyphicon-floppy-disk"></span> Add New</a>'


        matching_instructors = Instructor.objects.all().filter(aliases__icontains=instructor_name)
        if matching_instructors:
            result = ""
            for instr in matching_instructors:
                result = result+self.__build_html_link_to_instructor(instr, event)

            return result+add_link

        #instructor_sub_names = instructor_name.split(" ")
        instructor_sub_names = re.split(' |-',instructor_name)
        print ('divided/SPLIT name '+instructor_name+' into '+repr(instructor_sub_names))

        query = Q()
        if len(instructor_sub_names) > 1:
            #print "count is: "+repr(instructor_sub_names[0])+" "+repr(instructor_sub_names[1])

            #TODO: add loop here to search by all subnames, not just first two
            for sub_name in instructor_sub_names:
                query = query | Q(aliases__icontains=sub_name)
            #query = query | Q(aliases__icontains=instructor_sub_names[0])
            #query = query | Q(aliases__contains=instructor_sub_names[1])

            matching_instructors = Instructor.objects.all().filter(query)
            if matching_instructors:
                #link_url = reverse('admin:%s_%s_add' % ("schyoga", "instructor"))
                result = ""
                for instr in matching_instructors:
                    result = result+self.__build_html_link_to_instructor(instr, event)
                return result+add_link

        return add_link


    instr.allow_tags = True
    studio_link.allow_tags = True

    studio_link.short_description = "Studio"
    link_to_instructor.short_description = "!Do Not Use This Action!"

admin.site.register(Event, EventAdmin)