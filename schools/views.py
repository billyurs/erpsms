from schools.models import *
from django.shortcuts import render
from django.http.response import HttpResponse
#from developer_config_file import *
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
import logging
logger = logging.getLogger('erpsms')
logger_stats = logging.getLogger('erpsms_stats')
# Create your views here.


@staff_member_required
def addtenantdetails(request):
    """
    Stores the Tentant Details in TenantDetails Documents
    """
    if request.POST:
        tenantname = request.POST.get('tenantname', '')
        if tenantname:
            tenantid = tentant_details.get(tenantname, '')
            if tenantid:
                notes = request.POST.get('special_notes', '')
                #tenantjson = {'Total_students': request.POST.get('toatl_students', ''), 'address': request.POST.get('address', '')}
                tenobj = TenantDetails()
                tenobj.createobj(tenantid, tenantname, notes, tenantjson)

#@personal_member_required
# TODO : Need to write auth decorator

@login_required
def addstudentdetails(request):
    import pdb; pdb.set_trace()
    if request.POST:
        tenantid_of_req_user = request.user.tenantid
        if tenantid_of_req_user:
            personobj = Person()
            persondict = personobj.createobj(firstname=request.POST.get('firstname', ''), middlename=request.POST.get('middlename', ''),
                                             lasttname=request.POST.get('lasttname', ''), stduentid = request.POST.get('stduentid', '') email=request.POST.get('email', ''),
                                             phno=request.POST.get('phno', ''), gender=request.POST.get('gender', ''), address=request.POST.get('address', ''),
                                             peronjson=request.POST.get('peronjson', ''), notes=request.POST.get('notes', ''), tenantid=tenantid_of_req_user)
            studentobj = Student()
            parentjson = {'Parent_details': request.POST.get('parentjson', {})}
            studentobj.createobj(person=persondict, studentid=request.POST.get('studentid', ''),
                                 parentjson=parentjson, studentjson={}, notes=request.POST.get('notes', ''))
            logger_stats.info('Adding Student Details %s'%(request.POST))
    return render_to_response('form.html',
                              context_instance=RequestContext(request))

#@personal_member_required
# TODO : Need to write auth decorator


def addparentdetails(request):
    """
    To activate the Parent User and add student mapping
    """
    if request.POST:
        tenantid_of_req_user = request.user['tenantid']
        if tenantid_of_req_user:
            persondict = personobj.createobj(firstname=request.POST.get('firstname', ''), middlename=request.POST.get('middlename', ''),
                                             lasttname=request.POST.get('lasttname', ''), email=request.POST.get('email', ''),
                                             phno=request.POST.get('phno', ''), gender=request.POST.get('gender', ''), address=request.POST.get('address', ''),
                                             peronjson=request.POST.get('peronjson', ''), notes=request.POST.get('notes', ''), tenantid=tenantid_of_req_user)
            parentobj = Parent()
            studentjson = {
                'Student_details': request.POST.get('studentjson', {})}
            parentobj.createobj(personid=persondict, studentid=studentjson, parentjson=request.POST.get('parentjson', {}),
                                mobile=request.POST.get('mobile', ''), notes=request.POST.get('notes', ''), tenantid=tenantid_of_req_user)


def addteacherdetails(request):
    """
    To activate the Teacher User and class mapping
    """
    if request.POST:
        tenantid_of_req_user = request.user['tenantid']
        if tenantid_of_req_user:
            persondict = personobj.createobj(firstname=request.POST.get('firstname', ''), middlename=request.POST.get('middlename', ''),
                                             lasttname=request.POST.get('lasttname', ''), email=request.POST.get('email', ''),
                                             phno=request.POST.get('phno', ''), gender=request.POST.get('gender', ''), address=request.POST.get('address', ''),
                                             peronjson=request.POST.get('peronjson', ''), notes=request.POST.get('notes', ''), tenantid=tenantid_of_req_user)
            teacherobj = Teacher()
            teacherjson = {
                'Teacher_class': request.POST.get('teacherjson', {})}
            teacherobj.createobj(personid = persondict, teacheridemail= request.POST.get('email', ''),
                                 subjectdetails=request.POST.get('subjectdetails', {}), mobile=request.POST.get('mobile', ''),
                                 teacherjson=request.POST.get('teacherjson', {}), notes='', tenantid=tenantid_of_req_user)
