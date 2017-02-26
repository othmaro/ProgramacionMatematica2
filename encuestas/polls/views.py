from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
# Create your views here.

def index(request):
    template = loader.get_template('polls/index.html')
    context = {
    'variable': 'Esto es una variable'
    }
    return HttpResponse(template.render(context,request))
