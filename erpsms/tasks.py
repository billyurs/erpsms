# File to run the cron
from common.communicators import sendemail
import datetime
import settings
import os
def dailyLogReport():
	import pdb;  pdb.set_trace()
	workingdir = os.getcwd()
	# Attach erpsms, erpsms_stats
	erpsmsfilepath = '%s/erpsms/logs/erpsms.log'%(workingdir)
	erpsms_statsfilepath = '%s/erpsms/logs/erpsms_stats.log'%(workingdir)
	emailsub = 'Daily log report [erpms, erpsms_stats]'
	DateTime = ('Current Datetime %s'%(datetime.datetime.now()))
	emailbody = '<html><head>Report Generated DateTime: %s </head></html>'%(DateTime)
	to_mail = settings.DEFAULT_FROM_EMAIL
	attachmentlist = [erpsmsfilepath,erpsms_statsfilepath]
	sendemail(emailsub,emailbody,'',to_mail,attachmentlist)

	