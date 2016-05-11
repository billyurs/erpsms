from django.core.mail import send_mail, EmailMessage
import settings
default_from_email = settings.DEFAULT_FROM_EMAIL

def sendemail(email_subject, email_body, from_email, to_email, attachment = []):
    if not from_email:
        from_email = default_from_email
    if attachment:
        mail = EmailMessage(email_subject, email_body, from_email, to_email)
        for attachfile in attachment:
            mail.attach(attachfile, mail.read(), mail.content_type)
        mail.send()
    else:
        send_mail(email_subject, email_body, from_email, to_email, fail_silently=False)
