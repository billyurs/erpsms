from django.core.mail import send_mail, EmailMessage
from  erpsms.settings import DEFAULT_FROM_EMAIL
import logging

logger_stats = logging.getLogger('erpsms_stats')
default_from_email = DEFAULT_FROM_EMAIL

def sendemail(email_subject, email_body, from_email, to_email, attachment=[]):
    """
    API to send the email
    :param email_subject:
    :param email_body:
    :param from_email:
    :param to_email:
    :param attachment:
    :return:
    """
    if not from_email:
        from_email = default_from_email
    if attachment:
        mail = EmailMessage(email_subject, email_body, from_email, [to_email])
        for attachfile in attachment:
            mail.attach_file(attachfile, "text/html")
        mail.send()
    else:
        send_mail(email_subject, email_body, from_email, to_email, fail_silently=False)
    logger_stats.info('Email Subject:%s\tEmail Body:%s\tFrom Email:%s\tTo Email%s\t attachement %s' % (
    email_subject, email_body, from_email, to_email, attachment))
