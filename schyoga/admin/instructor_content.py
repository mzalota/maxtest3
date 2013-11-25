from django.contrib import admin
from django.forms import ModelForm, ModelChoiceField
from schyoga.models.instructor import Instructor
from schyoga.models.instructor_content import Instructor_Content


class InstructorModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s %s" % (obj.id, obj.instructor_name)


class Instructor_ContentAdminForm(ModelForm):
    instructor = InstructorModelChoiceField(queryset=Instructor.objects.all().order_by('id', 'instructor_name'))

    class Meta:
        model = Instructor_Content


class Instructor_ContentAdmin(admin.ModelAdmin):
    list_per_page = 250
    list_display = ('id', 'category')
    list_display_links = ('id', 'category')

    form = Instructor_ContentAdminForm


admin.site.register(Instructor_Content, Instructor_ContentAdmin)