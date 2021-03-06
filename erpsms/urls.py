from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView, TemplateView
from django.contrib import admin
admin.autodiscover()
import os
try:
    from erpsms.views import *
except:
    from views import *
from django.conf import settings
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
STATIC_PATH = PROJECT_PATH
urlpatterns = patterns('',
                       # Examples:
                       (r'^login', 'erpsms.views.login_user'),
                       (r'^dummy', 'erpsms.views.dummy'),
                       (r'^createuser$', 'erpsms.views.createuser'),
                       (r'^password_reset_req_activationkey$', 'erpsms.views.password_reset_send_activation_key'),
                       (r'^$', 'erpsms.views.home'),
                       (r'^accounts/confirm/(?P<activation_key>\w+)/', ('erpsms.views.register_confirm')),
                       (r'^accounts/password_reset/(?P<activation_key>\w+)/', ('erpsms.views.password_reset_validate_activation_key')),
                       # url(r'^blog/', include('blog.urls')),
                       (r'^autodeploy/', 'erpsms.views.autodeploy'),
                       (r'^usernamesuggestion','erpsms.views.usernamesuggestion'),
                       (r'^common/getcsrf','common.csrferpsmsdecorators.csrfforapi'),
                       url(r'^admin/', include(admin.site.urls)),
                       #url(r'^$', TemplateView.as_view(template_name="index.html")),

                       url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
                           {'document_root': STATIC_PATH + "/static/"}),
                       url(r'^(?P<path>.*\.txt)$', 'django.views.static.serve',
                           {'document_root': STATIC_PATH + "/"}),
                       url(r'^/static/avatars/(?P<path>.*)$', 'django.views.static.serve',
                           {'document_root': STATIC_PATH + '/static/avatars/', }),
                       url(r'', include('social_auth.urls')),
                       url(r'^accounts/facebook/login/', 'erpsms.views.facebookauthrequest'),
                       url(r'^accounts/google/login/', 'erpsms.views.googleauthrequest'),
                       url(r'^signin_login_success/', 'erpsms.views.signsuccess'),
                       url(r'^logout/', 'erpsms.views.logout_user'),
                       url(r'^allauth/accounts/', include('allauth.urls')),
                       #url('', include(
                        #   'social.apps.django_app.urls', namespace='social')),
                       #url(r'^$', 'schools.views.index', name='index'),
                       url('', include('django.contrib.auth.urls', namespace='auth')),
                       )
if 'schools' in settings.INSTALLED_APPS:
    urlpatterns += patterns('', url(r'^schools', include('schools.urls')))

if 'api' in settings.INSTALLED_APPS:
    urlpatterns += patterns('', url(r'^api', include('api.urls')))

