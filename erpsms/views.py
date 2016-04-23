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
import simplejson
import settings
import os

logger = logging.getLogger('erpsms')
logger_stats = logging.getLogger('erpsms_stats')
domain = settings.domain


def home(request):
    context = RequestContext(request,
                             {'request': request,
                              'user': request.user})
    return render_to_response('login.html',
                              context_instance=context)


def login_user(request):
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        flavor = request.POST.get('flavor', '')
        if user:
            if user.is_active:
                login(request, user)
                if flavor == 'android':
                    return HttpResponse(simplejson.dumps({'success': True, 'msg': "Login Success"}))
                return render_to_response('form.html', {}, context_instance=RequestContext(request))
        else:
            if flavor == 'android':
                return HttpResponse(
                    simplejson.dumps({'success': False, 'msg': "This username is not asscoicated with our system"}))
            return render_to_response('login.html', {}, context_instance=RequestContext(request))
    elif request.user.is_authenticated():
        return render_to_response('form.html', {}, context_instance=RequestContext(request))
    return render_to_response('login.html', {}, context_instance=RequestContext(request))


def index(request):
    if request.method == 'POST':
        try:
            import pdb
            pdb.set_trace()
            var = request.POST['var']
        except:
            print 'Where is my var?'
    return render_to_response('form.html', {}, context_instance=RequestContext(request))


def facebookauth(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponseRedirect('allauth/accounts/facebook/login/')


def usernamesuggestion(request):
    """
    Logic to suggest the available username
    """
    if request.POST:
        email = request.POST.get('username', '')
        if email:
            usrobj = get_or_none(model=CustomUser, email=email)
            if not usrobj:
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
                        return HttpResponse(returnmsg, content_type="text/plain")
                    returnmsg = "Email is not in correct format"
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
                            returnmsg += ' Available username is ' + \
                                         email + newusername
                            return HttpResponse(returnmsg, content_type="text/plain")
                else:
                    startno = 0
                    while (True):
                        startno += 1
                        usrobj = get_or_none(
                            model=CustomUser, email=email + str(startno))
                        if usrobj is None:
                            returnmsg += ' Available username is ' + \
                                         email + str(startno)
                            return HttpResponse(returnmsg, content_type="text/plain")
    return render_to_response('login.html', context_instance=RequestContext(request))


def createuser(request):
    username = password = ''
    if request.POST:
        username = request.POST['email']
        password = request.POST['password']
        email = request.POST['email']
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        activation_key = hashlib.sha1(salt + email).hexdigest()
        key_expires = datetime.datetime.today() + datetime.timedelta(2)
        userobj = CustomUser(email=email, password=password)
        userobj.set_password(password)
        userobj.activation_key = activation_key
        userobj.key_expires = key_expires
        userobj.is_active = 0
        userobj.save()
        # Send email with activation key
        email_subject = 'Account confirmation'
        email_body = "Hey %s, thanks for signing up. To activate your account, click this link within \
            48hours %s/accounts/confirm/%s" % (username, domain, activation_key)
        send_mail(email_subject, email_body, 'erp4forppl.com',
                  [email], fail_silently=False)
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
