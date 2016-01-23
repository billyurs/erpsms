__author__ = 'madhu'
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from flight.multifield import MultiSelectField
import string
from django.template.loader import render_to_string
import datetime
from notify import Notify
from django.contrib.auth.models import User,Group,UserManager
from django.db.models import F
from django.conf import settings
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from lib.history import models as historymodels

class TenantDetails(models.model):
    tenantdetails = models.CharField(db_index=True,max_length=100)

