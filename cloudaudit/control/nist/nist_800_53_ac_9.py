# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2011 Piston Cloud Computing, Inc.
#
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


from xml.dom.minidom import Document
from cloudaudit.control import nist
from cloudaudit.evidence_engine import lastlogon_notification
import urlparse


class NIST_800_53_ac9(nist.NIST_800_53_Control):

    """
    Control evidence gathering implementation for NIST 800-53 control AC-7

    AC-9:

    Control:  The information system notifies the user, upon successful
    logon (access), of the date and time of the last logon (access).

    Supplemental Guidance:  This control is intended to cover both
    traditional logons to information systems and general accesses
    to information systems that occur in other types of architectural
    configurations (e.g., service oriented architectures).

    Control Enhancements:

    (1) The information system notifies the user, upon successful
    logon/access, of the number of unsuccessful logon/access
    attempts since the last successful logon/access.

    (2) The information system notifies the user of the number of
    [Selection: successful logins/accesses; unsuccessful login/access
    attempts; both] during [Assignment: organization-defined time period].


    """

    evidence_gatherer = None
    control_title = "NIST 800-53 AC-9 Last Logon Notification Enabled"
    control_id = "ac/9"
    control_subtitle = "Last Logon Notification"
    time_updated = "Never"

    def __init__(self):
        super(self.__class__, self).__init__()
        self.xml_inventory = None
        self.logon_nofitications = None

    @property
    def evidence_url(self):
        path = self.control_path + "/lastlogin.xml"
        return urlparse.urlunsplit((self.scheme, self.__class__.net_loc,
                                    path, None, None))

    def get_evidence(self, req):
        if self.entries is None:
            self.entries = []

        super(NIST_800_53_ac9, self).get_evidence(req)

        if self.evidence_gatherer is None:
            self.evidence_gatherer = \
            lastlogon_notification.LastLoginNotification()

        self.maxlogins = self.evidence_gatherer.get_evidence()

        self.time_updated = "2010-01-13T18:30:02Z"

        newentry = {}

        newentry['title'] = \
        self.__class__.control_title

        newentry['link'] = self.evidence_url
        newentry['id'] = newentry['link']
        newentry['type'] = "application/xml"
        newentry['updated'] = self.time_updated
        newentry['summary'] = \
        "A list of the detected configurations "\
        + "for last logon notification" +\
        "per host indexed by IP address"

        newentry['author'] = [{'name':'Piston_CloudAudit', 'email':\
        'cloudaudit@pistoncloud.com'}]
        newentry['contributor'] = []

        self.entries.append(newentry)

    def get_manifest(self):
        if self.entries is None:
            self.get_evidence(None)

        xml_str = super(NIST_800_53_ac9, self).get_manifest(None)

        return xml_str

    def get_xml_inventory(self, req):
        if self.maxlogins is None:
            self.maxlogins = self.evidence_gatherer.get_evidence()

        self.xml_inventory = Document()
        doc = self.xml_inventory

        head_element = doc.createElement("maxUnsuccessfulLogins")

        doc.appendChild(head_element)

        for item in self.maxlogins.keys():
            element = doc.createElement("entry")

            ptext = self.doc.createTextNode(str(self.maxlogins[item]))

            element.setAttribute("ip", item)

            element.appendChild(ptext)
            head_element.appendChild(element)

        retval = head_element.toprettyxml(indent="  ")

        return retval

    def handle_request(self, req):

        req.url()

        return ""
