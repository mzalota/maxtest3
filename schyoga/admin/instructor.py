from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.html import format_html
from schyoga.bizobj.page import Page
from schyoga.models.instructor import Instructor
from schyoga.models.instructor_content import Instructor_Content

class Instructor_ConentInline(admin.StackedInline):
    model = Instructor_Content


class InstructorAdmin(admin.ModelAdmin):

    change_list_template = "admin/schyoga/instructor/change_list_filter_sidebar.html"
    search_fields = ['instructor_name','aliases']
    #list_filter = ('state_name_url',)

    list_per_page = 250

    list_display = ('id', 'state_name_url', 'instructor_name', 'link_to_schedyoga_site', 'studios_cnt', 'fb', 'content')
    list_display_links = ('id', 'instructor_name')
    #list_select_related = ['studio']

    raw_id_fields = ['studios']
    autocomplete_lookup_fields = {
        'm2m': ['studios'],
    }

    inlines = [
        Instructor_ConentInline,
    ]


    # define the related_lookup_fields
    #related_lookup_fields = {
    #    'fk': ['related_fk'],
    #    'm2m': ['related_m2m'],
    #}

    def content(self, obj):
        """
        @type obj: Instructor
        """
        content_cnt = obj.instructor_content_set.count()

        url = reverse('admin:%s_%s_changelist' % ("schyoga", "instructor_content"))
        url = url + "?instructor=" + str(obj.id)

        return format_html(
            '<a href="{0}" target="_blank" title="{0}"><span class="glyphicon glyphicon-star"></span>{1}</a>', url,
            content_cnt)


    def fb(self, obj):
        """
        @type obj: Instructor
        """
        fb_id = obj.fb_id
        if not fb_id:
            return "none"

        #/picture?width=20&height=20
        return format_html(
            '<a href="http://facebook.com/{0}"></a><img src="http://graph.facebook.com/{0}/picture?width=20&height=20"/></a>',
            fb_id)
        #return format_html('<a href="http://facebook.com/{0}"></a><img src="http://graph.facebook.com/{0}/picture?type=square"/></a>',fb_id)

    def studios_cnt(self, obj):
        """
        @type obj: Instructor
        """
        studio_count = obj.studio_set.count()

        url = reverse('admin:%s_%s_changelist' % ("schyoga", "studio"))
        url = url + "?instructor=" + str(obj.id)

        return format_html(
            '<a href="{0}" target="_blank" title="{0}"><span class="glyphicon glyphicon-star"></span>{1}</a>', url,
            studio_count)

    def link_to_schedyoga_site(self, obj):
        """
        @type obj: Instructor
        """
        evnt_cnt = obj.event_set.count()

        page = Page.createFromEnum(Page.ENUM_TEACHER_PROFILE)
        url = page.urlForTeacherPage(obj)
        return format_html(
            '<a href="{0}" target="_blank" title="{0}"><span class="glyphicon glyphicon-eye-open"></span> {1}</a>', url,
            evnt_cnt)


    studios_cnt.allow_tags = True
    studios_cnt.short_description = 'Studios'
    link_to_schedyoga_site.allow_tags = True
    link_to_schedyoga_site.short_description = 'SchYoga'
    fb.allow_tags = True
    fb.short_description = "FB"
    content.allow_tags = True
    content.short_description = "Content"


admin.site.register(Instructor, InstructorAdmin)