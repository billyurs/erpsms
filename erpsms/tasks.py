# File to run the cron
from common.communicators import sendemail
import datetime
import settings
import os
def dailyLogReport():
	workingdir = os.getcwd()
	# Attach erpsms, erpsms_stats
	erpsmsfilepath = '%s/erpsms/logs/erpsms.log'%(workingdir)
	erpsmsfilepath = '' if not os.path.isfile(erpsmsfilepath) else erpsmsfilepath
	erpsms_statsfilepath = '%s/erpsms/logs/erpsms_stats.log'%(workingdir)
	erpsms_statsfilepath = '' if not os.path.isfile(erpsms_statsfilepath) else erpsmsfilepath
	emailsub = 'Daily log report [erpms, erpsms_stats]'
	DateTime = ('Current Datetime %s'%(datetime.datetime.now()))
	emailbody = 'Report Generated DateTime: %s'%(DateTime)
	to_mail = settings.DEFAULT_FROM_EMAIL
	attachmentlist = [erpsmsfilepath,erpsms_statsfilepath]
	sendemail(emailsub,emailbody,'',to_mail,attachmentlist)

if __name__ == "__main__":
	dailyLogReport()