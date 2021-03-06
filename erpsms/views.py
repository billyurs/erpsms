from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.contrib.admin.views.decorators import staff_member_required
from django.http import *
from registration.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from validate_email import validate_email
import re
import hashlib
from django.conf import global_settings
import datetime
import random
from django.utils import timezone
from django.views.decorators.clickjacking import xframe_options_exempt
from common import erpsms_json as simplejson
import settings
import os
from django.views.decorators.csrf import ensure_csrf_cookie
from common.redis_wrapper import RedisWrapper

logger = logging.getLogger('erpsms')
logger_stats = logging.getLogger('erpsms_stats')
from django.views.decorators.csrf import csrf_protect

domain = settings.domain
from django.core.cache import  get_cache
rediscon = get_cache('localcache')

def home(request):
    context = RequestContext(request,
                             {'request': request,
                              'user': request.user})
    return render_to_response('login.html',
                              context_instance=context)



from functools import wraps
def http_basic_auth(func):
    @wraps(func)
    def _decorator(request, *args, **kwargs):
        from django.contrib.auth import authenticate, login
        if request.META.has_key('HTTP_AUTHORIZATION'):
            authmeth, auth = request.META['HTTP_AUTHORIZATION'].split(' ', 1)
            if authmeth.lower() == 'basic':
                auth = auth.strip().decode('base64')
                username, password = auth.split(':', 1)
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)
        return func(request, *args, **kwargs)
    return _decorator



def login_user(request):
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        flavor = get_flavor(request)
        logger_stats.info('login username %s and flavor %s' % (username, flavor))
        if user:
            if user.is_active:
                login(request, user)
                logger_stats.info('Logged in successfully , user %s and flavor %s' % (username, flavor))
                if flavor == 'android':
                    userdata = getuserparameters(request)
                    return HttpResponse(simplejson.dumps({'success': True, 'msg': "Login Success",'userdata':userdata}))
                return render_to_response('form.html', {}, context_instance=RequestContext(request))
        else:
            if flavor == 'android':
                return HttpResponse(
                    simplejson.dumps({'success': False, 'msg': "This username is not asscoicated with our system"}))
            return render_to_response('login.html', {}, context_instance=RequestContext(request))
    elif request.user.is_authenticated():
        return render_to_response('form.html', {}, context_instance=RequestContext(request))
    return render_to_response('login.html', {}, context_instance=RequestContext(request))

from django.contrib.auth.decorators import user_passes_test
@http_basic_auth
#@login_required
@user_passes_test(lambda u: u.is_superuser)
def dummy(request):
    return HttpResponse('poda')


def getuserparameters(request):
    """
    :param request:
    :return: The set of active departments active to user
    """
    cache_key = '%s'%(request.user)
    userjson = {}
    if cache_key:
        userdata = rediscon.get(cache_key)
        if not userdata:
            userdata = {}
            userjson['firstname'] = request.user.first_name
            userjson['username'] = request.user.username
            userjson['lastname'] = request.user.last_name
            userjson['email'] = request.user.email
            userjson['tenant'] = request.user.tenantid
            userdata['profile_data'] = userjson
            departjson = {}
            userdata['department'] = departjson
            userdata['gallery'] = {}
            userdata['events'] = {}
            userdata['meta'] = {}
            rediscon.set(cache_key,userdata)
        logger_stats.info('%s Cache key \t%s cache value\t'%(cache_key,userdata))
        return simplejson.dumps(userdata)


def facebookauthrequest(request):
    logger_stats.info('Facebook Auth Req %s' % (request))
    if request.user.is_authenticated():
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponseRedirect('allauth/accounts/facebook/login/')


def googleauthrequest(request):
    logger_stats.info('Google Auth Req %s' % (request))
    if request.user.is_authenticated():
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponseRedirect('allauth/accounts/google/login/')


def signsuccess(request):
    flavor = get_flavor(request)
    if flavor == 'android':
        return HttpResponse(simplejson.dumps({'success': True, 'msg': "Signin_Login_Success"}))
    else:
        return render_to_response('index.html')


def usernamesuggestion(request):
    """
    Logic to suggest the available username
    """
    if request.POST:
        email = request.POST.get('username', '')
        if email:
            usrobj = get_or_none(model=CustomUser, email=email)
            if not usrobj:
                logger_stats.info('Username is Available %s ' % (email))
                return HttpResponse("Username is Available", content_type="text/plain")
                # return "Username is Available"
            else:
                """
                Check whether the input is email or username, if email return error message
                """
                if '@' in email:
                    is_valid = validate_email(email)
                    if is_valid:
                        returnmsg = "Entered Email ID already taken "
                        logger_stats.info('Entered Email ID already taken  %s ' % (email))
                        return HttpResponse(returnmsg, content_type="text/plain")
                    returnmsg = "Email is not in correct format"
                    logger_stats.info('Email is not in correct format  %s ' % (email))
                    return HttpResponse(returnmsg, content_type="text/plain")
                returnmsg = "Entered username already taken " + email
                numlist = re.findall(r'\d+', email)
                if numlist:
                    replacenum = int(numlist[0])
                    while (True):
                        replacenum += 1
                        newusername = str(replacenum)
                        usrobj = get_or_none(
                            model=CustomUser, email=email + newusername)
                        if not usrobj:
                            returnmsg += '\n Available username is ' + \
                                         email + newusername
                            logger_stats.info(returnmsg)
                            return HttpResponse(returnmsg, content_type="text/plain")
                else:
                    startno = 0
                    while (True):
                        startno += 1
                        usrobj = get_or_none(
                            model=CustomUser, email=email + str(startno))
                        if not usrobj:
                            returnmsg += '\n Available username is ' + \
                                         email + str(startno)
                            logger_stats.info(returnmsg)
                            return HttpResponse(returnmsg, content_type="text/plain")
    return render_to_response('login.html', context_instance=RequestContext(request))


def createuser(request):
    username = password = ''
    if request.POST:
        flavor = get_flavor(request)
        username = request.POST['email']
        password = request.POST['password']
        email = request.POST['email']
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        activation_key = hashlib.sha1(salt + email).hexdigest()
        key_expires = datetime.datetime.today() + datetime.timedelta(2)
        userobj = CustomUser.objects.filter(email=email)
        if userobj:
            logger_stats.info('Email/Name %s already exist ' % (email))
            if flavor == 'android':
                return HttpResponse(
                    simplejson.dumps({'Success': False, 'message': 'Email/Name %s already exist ' % (email)}))
            return HttpResponse('Email/Name %s already exist ' % (email), content_type="text/plain")

        userobj = CustomUser(email=email, password=password)
        userobj.set_password(password)
        if '@' in email:
            userobj.is_active = 0
        else:
            userobj.is_active = 1
        userobj.activation_key = activation_key
        userobj.key_expires = key_expires
        try:
            userobj.save()
        except Exception, e:
            logger_stats.info('Error While saving the User Obj %s %s' % (email, e))
            # The below code should work both Android and web as well
            return simplejson.dumps(
                {'Success': False, 'message': 'System not able to create user with this %s id' % (email)})
            # Send email with activation key
        email_subject = 'Account confirmation'
        email_body = "Hey %s, thanks for signing up. To activate your account, click this link within \
            48hours %s/accounts/confirm/%s" % (username, domain, activation_key)
        if '@' in email:
            send_mail(email_subject, email_body, 'erp4forppl.com',
                      [email], fail_silently=False)
        logger_stats.info('The Username: %s created Successfully , please check mail to activate' % (username))
        if flavor == 'android':
            return HttpResponse(simplejson.dumps({'Success': True,
                                                  'message': 'The Username: %s created Successfully , please check mail to activate' % (
                                                  username)}))
        return render_to_response('index.html')
    return render_to_response('login.html', context_instance=RequestContext(request))


def register_confirm(request, activation_key):
    # check if user is already logged in and if he is redirect him to some
    # other url, e.g. home
    if request.user.is_authenticated():
        HttpResponseRedirect('/home')

    # check if there is UserProfile which matches the activation key (if not
    # then display 404)
    user_profile = get_object_or_404(CustomUser, activation_key=activation_key)

    # check if the activation key has expired, if it hase then render
    # confirm_expired.html
    if user_profile.key_expires < str(timezone.now()):
        return render_to_response('user_profile/confirm_expired.html')
    # if the key hasn't expired save user and set him as active and render
    # some template to confirm activation
    user_profile.is_active = True
    user_profile.activation_key = ''
    user_profile.save()
    user_profile.email_user()
    return render_to_response('email-confirmation.html')


def password_reset_send_activation_key(request):
    if request.POST:
        email_or_username = request.POST.get('username', '')
        user_profile = get_object_or_404(
            CustomUser, email=email_or_username)
        if user_profile:
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            activation_key = hashlib.sha1(salt + email_or_username).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(2)
            user_profile.activation_key = activation_key
            user_profile.key_expires = key_expires
            user_profile.is_active = 0
            user_profile.save()
            email_subject = 'Account Password Reset'
            username = user_profile.get_full_name()
            username = username if username else user_profile.email
            email = user_profile.email
            if email:
                email_body = "Hey %s, reset link. To activate your account, click this link within \
                48hours %s/accounts/password_reset/%s" % (username, domain, activation_key)
                send_mail(email_subject, email_body, 'erp4forppl.com',
                          [email], fail_silently=False)
                logger_stats.info('Username request the password reset %s %s' % (username, activation_key))
                return HttpResponse('{success:True , msg:"Reset link sent"')
        else:
            return HttpResponse('{success:false,msg:"This username is not asscoicated with our system"}')
    else:
        return render_to_response('login.html', context_instance=RequestContext(request))


def password_reset_validate_activation_key(request, activation_key):
    user_profile = get_object_or_404(CustomUser, activation_key=activation_key)
    if request.POST and user_profile:
        password = request.POST.get('password', '')
        if password:
            user_profile.set_password(password)
            user_profile.activation_key = ''
            user_profile.save()
            return HttpResponseRedirect('/password/reset/complete')
    elif user_profile:
        if user_profile.key_expires < str(timezone.now()):
            return render_to_response('user_profile/confirm_expired.html')
        return render_to_response('password_reset.html', context_instance=RequestContext(request))
    else:
        return render_to_response('login.html')


@staff_member_required
def autodeploy(request):
    """
    To pull from master and autodeploy at server end
    """
    import git
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        workingdir = os.getcwd()
        gitobj = git.cmd.Git(workingdir)
        resp = gitobj.pull('https://' + username + ':' + password + '@bitbucket.org/localhakcers/erpsms.git')
        logger_stats.info('The response from git %s ' % (resp))
        logger_stats.info('The Server is Restarting')
        # To install pip packages 
        python_package = request.POST['pythonpackage']
        try:
            if python_package:
                pip.main(['install', python_package])
                logger_stats.info('Python package installed successfully %s ' % (python_package))
        except Exception, e:
            logger_stats.info('Exception during installing the python package %s and error : %s' % (python_package, e))
        # Path of WSGI File
        fname = '/var/www/erpforppl_pythonanywhere_com_wsgi.py'
        if os.path.exists(fname):
            try:
                os.utime(fname, None)
                logger_stats.info('The server restarted successfully')
            except Exception, e:
                logger_stats.critical('Error %s' % (e))
        else:
            logger_stats.info('File not found so server failed to restart , file path : %s' % (fname))
        return HttpResponse("Auto Deploy Executed", content_type="text/plain")
    else:
        # To do Need to render correct Render
        render_to_response('password_reset.html', context_instance=RequestContext(request))


def get_flavor(request):
    if request.POST:
        return request.POST.get('flavor', '')
    else:
        return request.GET.get('flavor', '')


def logout_user(request):
    flavor = get_flavor(request)
    logout(request)
    if flavor == 'android':
        return HttpResponse(simplejson.dumps({'success': True, 'msg': "Logout_Success"}))
    else:
        #return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return HttpResponseRedirect('/')
