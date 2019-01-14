from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import RedirectView
from django.contrib.auth.decorators import login_required
from django.conf.urls import url, include
from django.http import HttpResponseRedirect

def homepage(request):
	return HttpResponseRedirect('/users')