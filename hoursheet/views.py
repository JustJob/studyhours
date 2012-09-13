# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from hoursheet.models import Person

def index(request):
  return render_to_response('hoursheet/index.html', {'people': Person.objects.all()})