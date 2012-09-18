# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from hoursheet.models import Person, Week, TimingEvent
import datetime
import pytz
import json

def getCurrentWeek():
  now = datetime.datetime.now(pytz.timezone('US/Central'))
  current = Week.objects.filter(start__lte = now,
                                end__gte = now)
  if len(current) == 1:
    return current[0]
  return None

def index(request):
  return render_to_response('hoursheet/index.html', {'people': Person.objects.all()})

def searchPerson(request):
  responseData = {'result':'failed'}
  thisPerson = Person.objects.filter(firstName__exact=request.GET['firstName'],
                                     lastName__exact=request.GET['lastName'])
  if(len(thisPerson) > 0):
    week = getCurrentWeek()
    lastLogins = []
    print week
    logins = TimingEvent.objects.filter(person__exact=thisPerson, 
                                            signedIn__gte=week.start, 
                                            signedOut__lte=week.end)[0:5]
    for login in logins:
      lastLogins.append({"start":login.start, 
                         "end": login.end, 
                         "hours": login.hours(),
                         "signedIn" : thisPerson.signedIn,
                         "name" : thisPerson.__unicode__()})
    print lastLogins

    responseData['firstName'] = request.GET['firstName']
    responseData['lastName'] = request.GET['lastName']
    responseData['hours'] = thisPerson[0].getCurrentHours(week.start, week.end)
    responseData['isSignedIn'] = thisPerson[0].signedIn
    responseData['lastLogins'] = lastLogins
    responseData['result'] = "success"
    print 'success'
    print json.dumps(responseData)

  return HttpResponse(json.dumps(responseData), mimetype="application/json")
