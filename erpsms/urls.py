from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView, TemplateView
from django.contrib import admin
admin.autodiscover()
import os
from django.conf import settings
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
STATIC_PATH = PROJECT_PATH
urlpatterns = patterns('',
                       # Examples:
                       #url(r'^$', 'views.home', name='home'),
                       (r'^login$', 'views.login_user'),
                       (r'^createuser$', 'views.createuser'),
                       (r'^$', 'views.home'),
                       (r'^usernamesuggestion','views.usernamesuggestion'),
                       (r'^accounts/confirm/(?P<activation_key>\w+)/', ('views.register_confirm')),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       #url(r'^$', TemplateView.as_view(template_name="index.html")),

                       url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
                           {'document_root': STATIC_PATH + "/static/"}),
                       url(r'^(?P<path>.*\.txt)$', 'django.views.static.serve',
                           {'document_root': STATIC_PATH + "/"}),
                       url(r'^/static/avatars/(?P<path>.*)$', 'django.views.static.serve',
                           {'document_root': STATIC_PATH + '/static/avatars/', }),
                       url(r'', include('social_auth.urls')),
                       url(r'^accounts/facebook/login/', 'views.facebookauth'),
                       url(r'^allauth/accounts/', include('allauth.urls')),

                       #url('', include(
                        #   'social.apps.django_app.urls', namespace='social')),
                       #url(r'^$', 'schools.views.index', name='index'),
                       url('', include('django.contrib.auth.urls', namespace='auth')),
                       )
if 'schools' in settings.INSTALLED_APPS:
    urlpatterns += patterns('', url(r'^schools', include('schools.urls')))
