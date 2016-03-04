from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView, TemplateView
from django.contrib import admin
from schools.views import *
admin.autodiscover()
import os
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
STATIC_PATH = PROJECT_PATH
urlpatterns = patterns('',
	(r'^/addstudent$', 'schools.views.addstudentdetails'),)
