from django.db import models
import datetime

# Create your models here.
class Person(models.Model):
  firstName = models.CharField(max_length=25)
  lastName = models.CharField(max_length=30)
  weeklyHours = models.IntegerField(default=12)
  currentFine = models.FloatField(default = 2.0)

  def isSignedIn(self):
    if(len(TimingEvent.objects.filter(person__exact=self, 
                                      signedOut__isnull=True))):
      return True
    else: return False

  def __unicode__(self):
    return self.firstName + " " + self.lastName

  def getCurrentHours(self, startTime, endTime):
    retval = 0.0;
    for time in TimingEvent.objects.filter(person__exact=self, 
                                           signedIn__gte=startTime, 
                                           signedOut__lte=endTime):
      retval += time.seconds()

    return float(int(retval/900)) / 4

class TimingEvent(models.Model):
  priorWeek = models.BooleanField(default=False)
  person = models.ForeignKey(Person)
  signedIn = models.DateTimeField(null=False)
  signedOut = models.DateTimeField(blank=True)

  def seconds(self):
    return (self.signedOut - self.signedIn).total_seconds()

  def hours(self):
    return float(int(self.seconds() / 900))/4

  def __unicode__(self):
    return self.person.__unicode__() + " TimingEvent"

  def save(self, *args, **kwargs):
    if not self.signedIn:
      self.signedIn = datetime.datetime.now()

    return super(TimingEvent, self).save()

class Week(models.Model):
  start = models.DateTimeField();
  end = models.DateTimeField();

  def __unicode__(self):
    return "week from " + str(self.start.month) + "/" + str(self.start.day) + "/" + str(self.start.year) + " to "\
      + str(self.end.month) + "/" + str(self.end.day) + "/" + str(self.end.year)

