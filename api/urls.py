from django.conf.urls import patterns, include, url
urlpatterns = patterns('',
 (r'/getweatherdetailsparser', 'api.views.getweatherdetailsparser'),
 )
