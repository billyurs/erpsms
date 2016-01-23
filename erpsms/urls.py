from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView, TemplateView
from django.contrib import admin
admin.autodiscover()
import settings

import os
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
STATIC_PATH = PROJECT_PATH
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'erpsms.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name="index.html")),

    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': STATIC_PATH+"/static/" }),
    url(r'^(?P<path>.*\.txt)$','django.views.static.serve', {'document_root': STATIC_PATH+"/"}),
    url(r'^/static/avatars/(?P<path>.*)$', 'django.views.static.serve',
                           {'document_root': STATIC_PATH + '/static/avatars/',}),


)

