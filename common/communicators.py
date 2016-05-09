from django.core.mail import send_mail, EmailMessage

def sendemail(email_subject,email_body,from_email,to_email,attchment, attachment = []):
	if attachment:
		mail = EmailMessage(email_subject, email_body, from_email, to_email)
		for attachfile in attachment:
	        attachfile.
	else:
		send_mail(email_subject,email_body,from_email,to_email,attchment,fail_silently=False)
	pass