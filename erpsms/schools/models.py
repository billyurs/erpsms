__author__ = 'madhu'
from common.mongo_wrapper import MongoWrapper


def getcolldetails(collectionobj, getattr, getval):
    """
    This function is to get the document from 
    """
    return collectionobj.find({getattr: getval})


def updatecolldetails(collectionobj, getattr='', getval='', obj=None, setattr=None, setval=None):
    if obj == None:
        collectionobj.update({getattr: getval},
                             {"$set": {setattr: setval}}, safe=True)
    else:
        collectionobj.update(
            {getattr: getval}, obj, safe=True)


def deletecolldetails(collectionobj, getattr, getval):
    collectionobj.remove({getattr: getval}, safe=True)


class TenantDetails(object):
    # To update the instance directly
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state
        self.tenantdetailscoll = MongoWrapper().get_mongo_collection(
            database='erpmongodb', collection='TenantDetails')

    def createobj(self, tenantid='', tenantname='', notes='', tenantjson={}):
        """
        This function is to insert the document into Tenant Details collection
        """
        tenantobj = {'tenantid': tenantid, 'tenantname': tenantname, 'notes': notes, 'tenantjson': tenantjson
                     }
        return tenantobj
    '''
    def getobj(self, getattr, getval):
        """
        This function is to get the document from 
        """
        return getmodeldetails(tenantdetailscoll, getattr, getval)

    def updateobj(self, getattr='', getval='', tenantobj=None, setattr=None, setval=None):
        updatecolldetails(
            tenantdetailscoll, getattr, getval, tenantobj, setattr, setval)

    def deleteobj(self, getattr, getval):
        deletecolldetails(tenantdetailscoll, getattr, getval)
    '''    

class Person(object):
    # To update the instance directly
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state
        self.persontdetailscoll = MongoWrapper().get_mongo_collection(
            database='erpmongodb', collection='Person')

    def createobj(self, firstname='', middlename='', lasttname='', email='', phno='', gender='', address='', peronjson={}, notes='', tenantid=''):
        """
        This function is to insert the document into Tenant Details collection
        """
        personobj = {'firstname': firstname, 'middlename': middlename, 'lasttname': lasttname, 'email': email, 'phno':
                     phno, 'gender': gender, 'address': address, 'peronjson': peronjson, 'notes': notes, 'tenantid': tenantid}
        self.persontdetailscoll.insert(tenantobj, safe=True)

    def getobj(self, getval, getattr):
        return getmodeldetails(persontdetailscoll, getattr, getval)

    def updateobj(self, getattr='', getval='', personobj=None, setattr=None, setval=None):
        updatecolldetails(
            self.persontdetailscoll, getattr, getval, personobj, setattr, setval)

    def deleteobj(self, getattr, getval):
        deletecolldetails(self.persontdetailscoll, getattr, getval)


class Student(object):
       # To update the instance directly
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state
        self.studentdetailscoll = MongoWrapper().get_mongo_collection(
            database='erpmongodb', collection='Student')

    def createobj(self, person='', studentid='', parentjson={}, studentjson={}, notes=''):
        studentobj = {'personid': personid, 'studentid': studentid, 'studentjson': studentjson, 'notes': notes, 'tenantid': tenantid}
        self.studentdetailscoll.save()

    def getobj(self, getval, getattr):
        return getmodeldetails(self.studentdetailscoll, getattr, getval)

    def updateobj(self, getattr='', getval='', personobj=None, setattr=None, setval=None):
        updatecolldetails(
            self.studentdetailscoll, getattr, getval, personobj, setattr, setval)

    def deleteobj(self, getattr, getval):
        deletecolldetails(self.studentdetailscoll, getattr, getval)


class Parent(object):
       # To update the instance directly
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state
        self.parentdetailscoll = MongoWrapper().get_mongo_collection(
            database='erpmongodb', collection='Parent')

    def createobj(self, personid='', studentid='', parentjson={}, mobile='', notes='', tenantid=''):
        parentjson = {'personid': personid, 'studentid': studentid, 'parentjson':
                      parentjson, 'mobile': mobile, 'notes': notes, 'tenantid': tenantid}
        self.parentdetailscoll.save()

    def getobj(self, getval, getattr):
        return getmodeldetails(self.parentdetailscoll, getattr, getval)

    def updateobj(self, getattr='', getval='', personobj=None, setattr=None, setval=None):
        updatecolldetails(
            self.parentdetailscoll, getattr, getval, personobj, setattr, setval)

    def deleteobj(self, getattr, getval):
        deletecolldetails(self.parentdetailscoll, getattr, getval)


class Teacher(object):
       # To update the instance directly
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state
        self.teacherdetailcoll = MongoWrapper().get_mongo_collection(
            database='erpmongodb', collection='Teacher')

    def createobj(self, personid='', teacheridemail='', subjectdetails={}, mobile='', teacherjson={}, notes='', tenantid='tenantid'):
        parentjson = {'personid': personid, 'teacheridemail': teacheridemail, 'subjectdetails':
                      subjectdetails, 'mobile': mobile, 'notes': notes, 'tenantid': tenantid, 'teacherjson': teacherjson}
        self.teacherdetailcoll.save()

    def getobj(self, getval, getattr):
        return getmodeldetails(self.parentdetailscoll, getattr, getval)

    def updateobj(self, getattr='', getval='', personobj=None, setattr=None, setval=None):
        updatecolldetails(
            self.teacherdetailcoll, getattr, getval, personobj, setattr, setval)

    def deleteobj(self, getattr, getval):
        deletecolldetails(self.teacherdetailcoll, getattr, getval)
