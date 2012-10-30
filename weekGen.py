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
  week = Week(start=now, end=end)
  now = now + datetime.timedelta(days=7)
  end = end + datetime.timedelta(days=7)
  week.save()

people = ['Adam Kosecki', 'Alex Delong', "Alex O'Neil", 'Andrew Baumen', 'Bret Payne', 'Cody Burgess', 'Cody Haislip', 'Corey Reuter', 'Dylan Alarcon', 'Gage Witt', 'Grant Luebbering', 'Jacob Francka', 'Jake Kistler', 'John Walsh', 'Joel Cardin', 'Jerek Nash', 'Josiah Enns', 'Kevin Walaszek', 'Lafe Windmiller', 'Logan Gesiler', 'Matt Achelpohl', 'Michael Keener', 'Ollie Naeger', 'Trevor Townsend', 'Brandon Gasser', 'Sam Manson', "Jimmy O'Donnel", 'Jeremy Satterfield', 'Josh Weber']
for person in people:
  thisperson = Person(firstName=person.split(' ')[0], lastName=person.split(' ')[1], weeklyHours=12, currentFine=2)
  thisperson.save()

people = ['Ryan Covington', 'Daniel FLing', 'Nick Slama', 'Kenny Holtz', 'Mason Smith']
for person in people:
  thisperson = Person(firstName=person.split(' ')[0], lastName=person.split(' ')[1], weeklyHours=6, currentFine=2)
  thisperson.save()

people = ['Eric Moore', 'Tiredej Bunyarataphantusadf', 'Brian Bakala', 'Jared Wyatt', 'Zach Boswell', 'Mark Bradshaw', 'Alex Miles']
for person in people:
  thisperson = Person(firstName=person.split(' ')[0], lastName=person.split(' ')[1], weeklyHours=7, currentFine=2)
  thisperson.save()