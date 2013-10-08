from copy import copy

from django import template
import pytz

from schyoga.bizobj.state import State

register = template.Library()
import datetime
from django.conf import settings

from django.template.defaultfilters import stringfilter


@register.inclusion_tag('snippet-top-nav.html', takes_context=True)
def show_top_nav(context):
    request = context['request']

    try:
        state_url_name = request.resolver_match.kwargs['state_url_name']
        state = State.createFromUrlName(state_url_name)
    except:
        state = State.createFromUrlName()

    if not state:
        state = State.createFromUrlName()

    #pass full copy of context to the template. sitetree will need it for resolving Instructor and Studio variable for constructing correct URLs
    inclusionContext = copy(context)
    inclusionContext.update({
        'state': state,
    })

    return inclusionContext


@register.assignment_tag
def events_from_calendar(o, eventDate, eventTime):
    try:
        return o.getEventsByDateAndTime(eventDate, eventTime)
    except:
        return settings.TEMPLATE_STRING_IF_INVALID


@register.filter(name='convert_fb_date')
@stringfilter
def convert_fb_date(dt_string):
    #parse the string and convert it to datetime object. Original format is: 2013-07-25T19:46:27+0000
    """

    :param dt_string:
    :return:
    """

    #TODO: validate that the passed sting is in GMT timezone. Deal with cases where the string is in different format
    dt = datetime.datetime.strptime(dt_string + 'GMT', "%Y-%m-%dT%H:%M:%S+0000%Z")
    #the string passed is in GMT. Convert it to the local time
    dt_localtime = pytz.utc.localize(dt)
    return dt_localtime


# @register.filter(name='get')
# def get(o, index):
#     try:
#         return o[index]
#     except:
#         return settings.TEMPLATE_STRING_IF_INVALID