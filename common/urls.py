__author__ = 'madhu'
from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView, TemplateView
from django.contrib import admin
admin.autodiscover()
import os
from erpsms.views import *
from django.conf import settings

urlpatterns = patterns('',
                       # Examples:
                       (r'^/getcsrf$', 'common.csrferpsmsdecorators.csrfforapi'),)