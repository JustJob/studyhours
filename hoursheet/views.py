# Create your views here.
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from hoursheet.models import Person, Week, TimingEvent
import datetime
import pytz
import json
import time

def index(request):
  if not request.user.is_authenticated():
    raise Http404
  
  return render_to_response('hoursheet/index.html', {'people': Person.objects.all(),
                                                     'context_instance':RequestContext(request)})


def searchPerson(request):
  if not request.user.is_authenticated():
    raise Http404

  responseData = {'result':'failed'}
  firstName = ''
  lastName = ''
  if(request.method == 'GET'):
    firstName = request.GET['firstName']
    lastName = request.GET['lastName']
  elif(request.method == 'POST'):
    firstName = request.POST['firstName']
    lastName = request.POST['lastName']

  thisPerson = Person.objects.filter(firstName__exact=firstName,
                                     lastName__exact=lastName)
  if(len(thisPerson) > 0):
    week = Week.getCurrentWeek()
    lastLogins = []
    logins = TimingEvent.objects.filter(person__exact=thisPerson, 
                                            signedIn__gte=week.start, 
                                            signedOut__lte=week.end)
    if(len(logins) > 5):
      logins = logins[0:5]

    for login in logins:
      lastLogins.append({"start":login.signedIn.strftime('%m/%d/%y %H:%M:%S %Z'), 
                         "end": login.signedOut.strftime('%m/%d/%y %H:%M:%S %Z'), 
                         "hours": login.hours()})
    print lastLogins

    responseData['firstName'] = firstName
    responseData['lastName'] = lastName
    responseData['hours'] = thisPerson[0].getCurrentHours(week)
    responseData['isSignedIn'] = thisPerson[0].isSignedIn()
    responseData['lastLogins'] = lastLogins
    responseData['result'] = "success"

  return HttpResponse(json.dumps(responseData), mimetype="application/json")

def signIn(request):
  if not request.user.is_authenticated():
    raise Http404

  if(request.method == "POST"):
    thisPerson = Person.objects.filter(firstName__exact=request.POST['firstName'],
                                       lastName__exact=request.POST['lastName'])
    if len(thisPerson) == 1:
      thisPerson = thisPerson[0]

    if not thisPerson.isSignedIn():
      signedIn = datetime.datetime.now(pytz.timezone('UTC'));
      event = TimingEvent(person=thisPerson, signedIn=signedIn)
      event.save()

  
  return searchPerson(request)

def timeFromMidnight(time):
  midnight = datetime.datetime(time.year, 
                               time.month,
                               time.day,
                               23,59,59)

  return float(int((midnight - time)/900)) / 4

def midnight(time):
  midnight = datetime.datetime(time.year, 
                               time.month,
                               time.day,
                               23,59,59)
  midnight.hour = 23
  midnight.minute = 59
  midnight.second = 59

  return midnight

def signOut(request):
  if not request.user.is_authenticated():
    raise Http404
    
  if(request.method == "POST"):
    thisPerson = Person.objects.filter(firstName__exact=request.POST['firstName'],
                                       lastName__exact=request.POST['lastName'])

    event = TimingEvent.objects.filter(person__exact=thisPerson[0], 
                                        signedOut__isnull=True)
    print event

    if(len(thisPerson) == 1 and len(event) == 1):
      thisPerson = thisPerson[0]
      event = event[0]

      now = datetime.datetime.now(pytz.timezone('UTC'))
      inThisWeek = Week.getCurrentWeek(False, event.signedIn)
      inPriorWeek = Week.getCurrentWeek(True, event.signedIn)
      outThisWeek = Week.getCurrentWeek(False, now)
      outPriorWeek = Week.getCurrentWeek(True, now)

      if inThisWeek.pk == inPriorWeek.pk: #if signed in on a weekday
        if outThisWeek.pk == outPriorWeek.pk:
          event.signedOut = now
        else: #if signed in on weekday and signed out on sunday
          hoursWithThis = thisPerson.getCurrentHours(outPriorWeek) + timeFromMidnight(event.signedIn)
          if hoursWithThis >= thisPerson.weeklyHours:
            event.signedOut = outPriorWeek.end
            newEvent = TimingEvent(person=thisPerson, signedIn=outThisWeek.start, signedOut=now)
            newEvent.save()
          else: #if they need this current sunday session to be counted for the prior week
            event.priorWeek = True
            event.signedOut = now
      else:
        hours = thisPerson.getCurrentHours(outPriorWeek)
        if outThisWeek.pk == outPriorWeek.pk:
          if hours >= thisPerson.weeklyHours:
            event.signedOut = now
          else:
            newEvent = None;
            event.priorWeek = True
            if hours + timeFromMidnight(now) < thisPerson.weeklyHours:
              event.signedOut = inPriorWeek.end

              newEvent = TimingEvent(person=thisPerson, 
                                     signedIn=midnight(outPriorWeek.start), 
                                     signedOut=now)
            else:
              timeNeeded = datetime.timedelta(hours=(thisPerson.weeklyHours - hours))
              event.signedOut = event.signedIn + timeNeeded
              newEvent = TimingEvent(person=thisPerson,
                                     signedIn=event.signedOut,
                                     signedOut=now)
            newEvent.save()
        else:
          if hours >= thisPerson.weeklyHours:
            event.signedOut = now
          else:
            event.priorWeek = True
            if hours + timeFromMidnight(now) < thisPerson.weeklyHours:
              event.signedOut = now
            else:
              timeNeeded = datetime.timedelta(hours=(thisPerson.weeklyHours - hours))
              event.signedOut = event.signedIn + timeNeeded
              newEvent = TimingEvent(person=thisPerson,
                                     signedIn=event.signedOut,
                                     signedOut=now)
              newEvent.save()

      event.save()

  return searchPerson(request)
