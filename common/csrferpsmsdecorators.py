__author__ = 'madhu'
from django.utils.crypto import constant_time_compare, get_random_string

CSRF_KEY_LENGTH = 32
import simplejson
import logging
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger('erpsms')
logger_stats = logging.getLogger('erpsms_stats')


def _get_new_csrf_key():
    return get_random_string(CSRF_KEY_LENGTH)
@csrf_exempt
def csrfforapi(request):
    try:
        if request.POST:
            if request.POST.get('flavor', '') == 'android':
                request.META["CSRF_COOKIE"] = _get_new_csrf_key()
            request.META["CSRF_COOKIE_USED"] = True
            logger_stats.critical('CSRF Sent for Android %s' % (request.META))
            csrf = request.META['CSRF_COOKIE']
            return HttpResponse(simplejson.dumps({'token': csrf}))
        else:
            return HttpResponse(simplejson.dumps({'request': {}}))
    except:
        return  HttpResponse(simplejson.dumps({'request': {}}))
