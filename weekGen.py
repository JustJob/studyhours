#generates weeks for study hours

import datetime
import pytz
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'studyhours.settings'

from hoursheet.models import Person, Week, TimingEvent

today = datetime.date.today()
dayoffset = today.weekday()
now = datetime.datetime(today.year, today.month, today.day,tzinfo=pytz.timezone('US/Central'))
now = now + datetime.timedelta(days = -1 * (dayoffset + 1))
end = datetime.datetime(now.year,now.month,now.day,23,59,59, tzinfo=pytz.timezone('US/Central'))
end = end + datetime.timedelta(days=7)

for x in xrange(15):
  print "now is ", now
  print "end is ", end
  now = now + datetime.timedelta(days=7)
  end = end + datetime.timedelta(days=7)
  week = Week(start=now, end=end)
  week.save()
