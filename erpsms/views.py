from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
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
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/main/')

    return render_to_response('login.html', {}, context_instance=RequestContext(request))


def index(request):
    if request.method == 'POST':
        try:
            import pdb
            pdb.set_trace()
            var = request.POST['var']
        except:
            print 'Where is my var?'
    return render_to_response('simple.html', {}, context_instance=RequestContext(request))


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
            if usrobj is None:
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
                    while(True):
                        replacenum += 1
                        newusername = str(replacenum)
                        usrobj = get_or_none(
                            model=CustomUser, email=email + newusername)
                        if usrobj is None:
                            returnmsg += ' Available username is ' + \
                                email + newusername
                            return HttpResponse(returnmsg, content_type="text/plain")
                else:
                    startno = 0
                    while(True):
                        startno += 1
                        usrobj = get_or_none(
                            model=CustomUser, email=email + str(startno))
                        if usrobj is None:
                            returnmsg += ' Available username is ' + \
                                email + str(startno)
                            return HttpResponse(returnmsg, content_type="text/plain")
    return render_to_response('login.html', {}, context_instance=RequestContext(request))


def createuser(request):
    username = password = ''
    import pdb
    pdb.set_trace()
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
        userobj.save()
         # Send email with activation key
        email_subject = 'Account confirmation'
        email_body = "Hey %s, thanks for signing up. To activate your account, click this link within \
            48hours http://madhu.erpforppl.com:8000/accounts/confirm/%s" % (username, activation_key)
        send_mail(email_subject, email_body, 'erp4forppl.com',
                  [email], fail_silently=False)
        #user = authenticate(username=username, password=password)
        '''
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/main/')
        '''
    return render_to_response('login.html', {}, context_instance=RequestContext(request))


def register_confirm(request, activation_key):
    # check if user is already logged in and if he is redirect him to some
    # other url, e.g. home
    import pdb
    pdb.set_trace()
    if request.user.is_authenticated():
        HttpResponseRedirect('/home')

    # check if there is UserProfile which matches the activation key (if not
    # then display 404)
    user_profile = get_object_or_404(CustomUser, activation_key=activation_key)

    # check if the activation key has expired, if it hase then render
    # confirm_expired.html
    if user_profile.key_expires < timezone.now():
        return render_to_response('user_profile/confirm_expired.html')
    # if the key hasn't expired save user and set him as active and render
    # some template to confirm activation
    user_profile.is_active = True
    user_profile.activation_key = ''
    user_profile.save()
    return render_to_response('login.html')
