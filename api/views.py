from django.http import HttpResponse
from common import erpsms_json as simplejson

def temp(request):
	return HttpResponse(request.META)