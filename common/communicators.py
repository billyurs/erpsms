from django.core.mail import send_mail, EmailMessage

def sendemail(email_subject,email_body,from_email,to_email,attchment, attachment = []):
	if attachment:
		pass
	pass