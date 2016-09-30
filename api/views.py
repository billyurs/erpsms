from django.http import HttpResponse
from common import erpsms_json as simplejson
from erpsms.settings import WEATHER_APP_ID
from common.redis_wrapper import RedisWrapper
import time
from datetime import datetime
import urllib2
import copy
import traceback
import logging
logger = logging.getLogger('erpsms')
logger_stats = logging.getLogger('erpsms_stats')
from django.core.cache import  get_cache
rediscon = get_cache('localcache')


def weatherAPICall(urlreq):
    return urllib2.urlopen(urlreq)


def current_time_to_string(systemtime):
    current_time =('%s' % (systemtime)).split('.')[0]
    current_time_text = datetime.fromtimestamp(
        int(current_time)).strftime('%Y-%m-%d %H')
    return current_time_text

def get_place_name_by_lat_long(lat,lon):
    place_name = None
    req_url = ('http://maps.googleapis.com/maps/api/geocode/json?latlng=%s,%s&sensor=false' % (lat, lon))
    response = urllib2.urlopen(req_url)
    place_response = simplejson.loads(response.read())
    if place_response.get('status') == 'OK':
        place_name = place_response['results'][1]['address_components'][0]['long_name']
    return place_name


def getweatherdetailsparser(request):
    try:
        forcast = request.GET.get('days', '')
        if not forcast:
            forcast = request.GET.get('hourly', '')
        place_name_text = request.GET.get('place', '')
        latitude = request.GET.get('lat', '')
        longitutde = request.GET.get('lon', '')
        if not place_name_text:
            place_name_text = get_place_name_by_lat_long(latitude, longitutde)
        # Current system time
        current_time = current_time_to_string(time.time())
        if place_name_text:
            cache_key = place_name_text + '_' + current_time
            import pdb; pdb.set_trace()
            cache_dict = rediscon.get(cache_key)
            if not cache_dict:
                req_url = 'http://api.openweathermap.org/data/2.5/forecast/' + forcast + \
                          '?q=' + place_name_text + '&mode=json&units=metric&cnt=7&appid=' \
                          + WEATHER_APP_ID
                response = weatherAPICall(req_url)
                weatherresp = simplejson.loads(response.read())
                city_json = weatherresp.get('city', {})
                city_name = city_json['name']
                weatherjson = {'name': city_name, 'lat': city_json.get('coord', {}).get('lat', 0),
                               'lon': city_json.get('coord', {}).get('lon', 0)
                               }
                rediscon.set(city_name, weatherjson)
                for weatherdetjson in weatherresp.get('list', []):
                    weather_server_time = weatherdetjson.get('dt', 0)
                    cache_key = city_name + current_time_to_string(weather_server_time)
                    rediscon.set(cache_key, weatherdetjson)
                response_to_client = formweatherjson(weatherresp.get('list', ''))
            else:
                response_to_client = formweatherjson(cache_dict('list', ''))
        else:
            logger_stats.critical('%s\t%s\t%s\t%s\t'%('Not Able to retrieve place name', '',request.GET,''))
            return HttpResponse(simplejson.dumps({'Status':'Failed','Reason':'Not Able to retrieve place name'}))
        logger_stats.info('%s\t%s\t%s\t%s\t'%(response_to_client,request.GET,'',''))
        return HttpResponse(simplejson.dumps(response_to_client))
    except:
        formatted_lines = traceback.format_exc().splitlines()
        logger_stats.critical('%s\t%s\t%s\t%s\t'%(formatted_lines, '',request.GET,''))
        return HttpResponse(simplejson.dumps({'Status': 'Failed', 'Reason': 'Exception Occured at Server End',
                                              'Exception': formatted_lines}))

def formweatherjson(weatherdetails):
    responsejson = {}
    responselist = []
    for weatherdetobj in weatherdetails:
        systemtime = weatherdetobj.get('dt', 0)
        systemtime_text = current_time_to_string(systemtime)
        responsejson['time'] = systemtime_text
        responsejson['main'] = weatherdetobj.get('weather', {})[0].get('main', '')
        responsejson['description'] = weatherdetobj.get('weather', {})[0].get('description', '')
        tempdict = weatherdetobj.get('temp', {})
        if tempdict:
            # Client opts for whole day
            responsejson['max_temp'] = tempdict.get('max', '')
            responsejson['min_temp'] = tempdict.get('min', '')
            responsejson['morning_temp'] = tempdict.get('morn', '')
            responsejson['night_temp'] = tempdict.get('night', '')
            responsejson['day_temp'] = tempdict.get('day', '')
            responsejson['evening_temp'] = tempdict.get('eve', '')
        else:
            responsejson['max_temp'] = weatherdetobj.get('main', {}).get('temp_max', '')
            responsejson['temp_min'] = weatherdetobj.get('main', {}).get('temp_min', '')
        responselist.append(copy.copy(responsejson))
    return responselist
