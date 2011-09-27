__author__ = 'joshd'



import webob
from cloudaudit.api.InitControl import InitController
import cloudaudit.api.Evidence_MaxLoginAttempts
from xml.dom.minidom import Document


class Control_Nist800_53_AC_7(InitController):

    """
    Control evidence gathering implementation for NIST 800-53 control AC-7

    AC-7:

    Control:  The information system:
        a. Enforces a limit of [Assignment: organization-defined number] consecutive invalid access
        attempts by a user during a [Assignment: organization-defined time period]; and

        b. Automatically [Selection: locks the account/node for an [Assignment: organization-defined
        time period]; locks the account/node until released by an administrator; delays next login
        prompt according to [Assignment: organization-defined delay algorithm]] when the
        maximum number of unsuccessful attempts is exceeded.  The control applies regardless of
        whether the login occurs via a local or network connection.
    """

    def __init__(self):
        super(Control_Nist800_53_AC_7, self).__init__()
        
        self.evidenceGatherer = None
        self.regime_str = "NIS 800-53"
        self.control_title = "NIS 800-53 AC-7 Maximum Unsuccessful Logins"
        self.regime = "gov/nist/crc/sp800-53"
        self.regime_version = "r3"
        self.control_id = "ac/7"
        self.control_subtitle = "Max Unsuccessful Logins before Lockout"
        self.time_updated = None
        self.xmlInventory = None

        self.maxlogins = None


    def getEvidence(self, req):
        if self.entries == None:
            self.entries = [ ]
            
        super(Control_Nist800_53_AC_7, self).getEvidence(req)
        
        if self.evidenceGatherer == None:
           self.evidenceGatherer = cloudaudit.api.Evidence_MaxLoginAttempts.Evidence_MaxLoginAttempts()

        self.maxlogins = self.evidenceGatherer.getEvidence()

        self.time_updated = "2010-01-13T18:30:02Z"

        newentry = { }

        newentry['title'] = "Maximum Unsuccessful Logins Inventory for all Unix systems"
        newentry['link'] = self.rootUrl + "/" + self.regime + "/" + self.regime_version + "/" + self.control_id + "/" + "maxlogins.xml"
        newentry['id'] = newentry['link']
        newentry['type'] = "application/xml"
        newentry['updated'] = self.time_updated
        newentry['summary'] = "A list of the detected maximum number of allowable unsuccessful login attempts before account lockout per host indexed by IP address"
        newentry['author'] = [ { 'name' : 'Piston_CloudAudit' , 'email' : 'cloudaudit@pistoncloud.com' } ]
        newentry['contributor'] = [ ]
        


        self.entries.append(newentry)

        
    def getManifest(self):
        if self.entries == None:
            self.getEvidence(None)

        xmlStr = super(Control_Nist800_53_AC_7, self).getManifest(None)

        return xmlStr


    def getXmlInventory(self, req):
        if self.maxlogins == None:
            self.maxlogins = self.evidenceGatherer.getEvidence()

        self.xmlInventory = Document()
        doc = self.xmlInventory

        headElement =  doc.createElement("maxUnsuccessfulLogins")

        doc.appendChild(headElement)

        for item in self.maxlogins.keys():
            element = doc.createElement("entry")

            ptext = self.doc.createTextNode(str(self.maxlogins[item]))

            element.setAttribute("ip", item)

            element.appendChild(ptext)
            headElement.appendChild(element)

        retval = headElement.toprettyxml(indent="  ")

        return retval

    def HandleRequest(self, req):

        req.url()


        return ""
