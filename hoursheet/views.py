# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
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
  return render_to_response('hoursheet/index.html', {'people': Person.objects.all(),
                                                     'context_instance':RequestContext(request)})

def searchPerson(request):
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
    week = getCurrentWeek()
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

    responseData['firstName'] = firstName
    responseData['lastName'] = lastName
    responseData['hours'] = thisPerson[0].getCurrentHours(week.start, week.end)
    responseData['isSignedIn'] = thisPerson[0].isSignedIn()
    responseData['lastLogins'] = lastLogins
    responseData['result'] = "success"

  return HttpResponse(json.dumps(responseData), mimetype="application/json")

def signIn(request):
  print 'signing in'
  if(request.method == "POST"):
    thisPerson = Person.objects.filter(firstName__exact=request.POST['firstName'],
                                       lastName__exact=request.POST['lastName'])
    if len(thisPerson) == 1:
      thisPerson = thisPerson[0]

    if not thisPerson.isSignedIn():
      signedIn = datetime.datetime.now(pytz.timezone('US/Central'));
      event = TimingEvent(person=thisPerson, signedIn=signedIn)
      event.save()

  
  return searchPerson(request)

def signOut(request):
  print 'signing out'
  if(request.method == "POST"):
    thisPerson = Person.objects.filter(firstName__exact=request.POST['firstName'],
                                       lastName__exact=request.POST['lastName'])

    event = TimingEvent.objects.filter(person__exact=thisPerson[0], 
                                        signedOut__isnull=True)
    print event

    if(len(thisPerson) == 1 and len(event) == 1):
      event[0].signedOut = datetime.datetime.now(pytz.timezone('US/Central'))
      event[0].save()

  return searchPerson(request)
