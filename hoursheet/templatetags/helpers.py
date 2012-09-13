from django import template
import pytz
import datetime

register = template.Library()

@register.filter()
def getHours(value):
  end = datetime.datetime.now(pytz.timezone('US/Central'))
  return value.getCurrentHours(datetime.datetime(2012,1,1, tzinfo=end.tzinfo), end)
