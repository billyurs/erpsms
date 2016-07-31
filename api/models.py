from django.db import models
from registration.models import CustomUser
from erpsms.erpsms.multifield import MultiSelectField

class Farmingdetails(models.Model):
    name = models.CharField(db_index=True, max_length=10)
    url = models.CharField(max_length=100, db_index=True, null=True, blank=True)
    createdon = models.DateTimeField(auto_now_add=True)
    info = models.IntegerField(default=0, null=False)
    search_key = models.CharField(max_length=10)


class CrawlerURls(models.Model):
    name = models.CharField(db_index=True, max_length=10)
    url = models.CharField(max_length=100, db_index=True, null=True, blank=True)
    createdon = models.DateTimeField(auto_now_add=True)


def get_user_type_choices():
    return (
        ('Farmer', 'Farmer'),
        ('Sales Agent', 'Sales Agent'),
        ('Delivery Agent', 'Delivery Agent'),
        ('Bank Emp', 'Bank Emp'),
        ('CRM Executive', 'CRM Executive'),
        ('Farming Labour', 'Farming Labour'),
    )


class UserInfo(models.Model):
    userid = models.ForeignKey(CustomUser)
    farming_interest = models.CharField(db_index=True, max_length=10)
    crop_place = models.CharField( max_length=10)
    user_customization = models.TextField(null=False)
    type_of_user = models.CharField(
        max_length=100, null=False, db_index=True, choices=get_user_type_choices())

class PushNotification(models.Model):
    userid = models.ForeignKey(UserInfo)
    # Rain , Sun, wind etc User can add multi parameters
    user_preferences = MultiSelectField(max_length=500,choices=(('------','------'),))
    '''
    {'NotifyMe':4 #Before 4 hours system should notify '
      '' }
    '''
    notifyme = models.BooleanField(null=False,default=False)
    user_prefernces_customization = models.TextField(null=False)
    last_notified = models.DateTimeField(auto_now_add=True)