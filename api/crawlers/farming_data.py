__author__ = 'madhu'
from api.models import PushNotification, UserInfo
import time
from api.views import current_time_to_string
from api.views import getweatherdetailsparser
from django.http import QueryDict
from registration.models import CustomUser

class FarmingBaseClass(object):
    def __init__(self):
        pass

    def send_push_notification_to_user(self, request=None):
        """
        This function is cron to Notify user
        :param request:
        :return:
        """
        pushnotifyobjs = PushNotification.objects.all()
        for pushobj in pushnotifyobjs:
            if pushobj.notifyme:
                userobj = pushobj.userid
                current_time = current_time_to_string(time.time())
                place = userobj.crop_place
                last_notified = current_time_to_string(pushobj.last_notified)
                user_prefernces_customization = pushobj.user_prefernces_customization
                notify_preference_time = user_prefernces_customization.get('NotifyMe', 0)
                # Rani, heavy Rain list
                user_prefernces = pushobj.user_preferences
                if notify_preference_time + last_notified < current_time:
                    QueryDictvar = QueryDict('', mutable=True)
                    request.GET._mutable = True
                    QueryDictvar['hourly'] = 'hourly'
                    QueryDictvar['place'] = place
                    weatherresp = getweatherdetailsparser(request)
                    for serverresp in weatherresp:
                        if serverresp.get('main') in user_prefernces:
                            pass
                            #
                        else:
                            continue
                            # Construct the

    def farmer_notify_registration(self, request):
        """
        :param request:
        :return:
        """
        user_preferences = request.GET.get('user_preferences', 0)
        user_id = request.GET.get('userid', '')
        user_id = CustomUser.objects.get(email=user_id)
        notify_time = request.GET.get('notifytime', '')
        user_preferences_customization = {'NotifyMe', notify_time}
        userobj = UserInfo.objects.get(userid=user_id)
        kwargs = {'userid': userobj, 'user_preferences': user_preferences, 'notifyme': True,
                  'user_prefernces_customization': user_preferences_customization}
        pushnotifyobj = PushNotification(**kwargs)
        pushnotifyobj.save()

    def main_display_info(self,request):
        """
        Need to get
        :param request:
        :return:
        """
        pass