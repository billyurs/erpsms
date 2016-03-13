# appname/models.py

from django.db import models
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
import logging
logger = logging.getLogger('erpsms')
logger_stats = logging.getLogger('erpsms_stats')

def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.filter(*args, **kwargs)
    except model.DoesNotExist:
        return None

class CustomUserManager(BaseUserManager):

    def _create_user(self, email, password,
                     is_staff=False, is_superuser=False, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        import pdb; pdb.set_trace()
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        logger.info("Email tried to create user"+email)
        #Checking user  already exist or not
        username = extra_fields.get('username', '')
        if not username:
            username = email
        user = get_or_none(model = CustomUser,email = email)
        if not user:
            user = CustomUser(email=email,
                              is_staff=is_staff, is_active=True,
                              is_superuser=is_superuser, last_login=now,
                              date_joined=now, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    A fully featured User model with admin-compliant permissions that uses
    a full-length email field as the username.

    Email and password are required. Other fields are optional.
    """
    #import pdb; pdb.set_trace()
    email = models.EmailField(_('email address'), max_length=254, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    tenantid = models.CharField(_('tenant id'), max_length=30, blank=True)
    username = models.CharField(_('user name'), max_length=30, blank=True)
    deptname = models.CharField(_('Department name'), max_length=30, blank=True)
    activation_key = models.CharField(_('Activation Key'), max_length=300, blank=True)
    key_expires = models.CharField(_('Key expires'), max_length=300, blank=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject='', message='', from_email=None):
        """
        Sends an email to this User.
        """
        subject = 'Thanks for joining with us'
        message = "Test Mail madhu here"
        from_email = 'erp4ppl@gmail.com'
        if self.email and self.is_active:
            send_mail(subject, message, from_email, [self.email])
