from django.db import models

# Create your models here.
class Person(models.Model):
  firstName = models.CharField(max_length=25)
  lastName = models.CharField(max_length=30)
  weeklyHours = models.IntegerField(default=12)
  currentFine = models.FloatField(default = 2.0)
  signedIn = models.BooleanField(default=True)

  def __unicode__(self):
    return self.firstName + " " + self.lastName

  def getCurrentHours(startTime, endTime):
    retval = 0.0;
    for(time in TimingEvent.objects.filter(person__exact=self, 
                                           signedIn__gte=startTime, 
                                           signedOut__lte=endTime)):
      retval += time.total_seconds()

    return retval

class TimingEvent(models.Model):
  person = models.ForeignKey(Person)
  signedIn = models.DateTimeField(auto_now_add=True)
  signedOut = models.DateTimeField(null=True)

  def timeDifference():
    if(signedOut)

  def __unicode__(self):
    return self.person + " TimingEvent"

