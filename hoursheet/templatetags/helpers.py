from django import template
from hoursheet.models import TimingEvent
import pytz
import datetime

register = template.Library()

@register.filter()
def getHours(value):
  end = datetime.datetime.now(pytz.timezone('US/Central'))
  event = TimingEvent.objects.filter(person__exact=value, 
                                     signedOut__isnull=True)
  if len(event) > 1:
    print 'something went wrong... very very wrong'
    return -1
  elif len(event) == 0:
    print value.firstName, ' ', value.lastName, ' not signed in'
    return 0

  event = event[0]
  return ((int)((end - event.signedIn).total_seconds()/3600*10000))/10000.0
  


