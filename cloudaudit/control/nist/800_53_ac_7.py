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
from cloudaudit.control import base
from cloudaudit.evidence import max_login_attempts


class NIST_800_53_ac7(base.BaseControl):
    """
    Control evidence gathering implementation for NIST 800-53 control AC-7

    AC-7:

    Control:  The information system:
        a. Enforces a limit of [Assignment: organization-defined number]
        consecutive invalid access
        attempts by a user during a [Assignment: organization-defined
        time period]; and

        b. Automatically [Selection: locks the account/node for an [Assignment:
        organization-defined time period];
        locks the account/node until released by an administrator;
        delays next login prompt according to [Assignment: organization-
        defined delay algorithm]] when the maximum number of unsuccessful
        attempts is exceeded.

        The control applies regardless of whether the login occurs via a
        local or network connection.
    """

    control_title = "NIS 800-53 AC-7 Maximum Unsuccessful Logins",
    control_id = "ac/7",
    control_subtitle = "Max Unsuccessful Logins before Lockout",

    def __init__(self):
        super(self.__class__, self).__init__()
        self.xml_inventory = None
        self.max_logins = None

    def get_evidence(self, req):
        if self.entries is None:
            self.entries = []

        super(NIST_800_53_ac7, self).get_evidence(req)

        if self.evidence_gatherer is None:
            self.evidence_gatherer = max_login_attempts.MaxLoginAttempts

        self.maxlogins = self.evidence_gatherer.get_evidence()

        self.time_updated = "2010-01-13T18:30:02Z"

        newentry = {}

        newentry['title'] = \
        "Maximum Unsuccessful Logins Inventory for all Unix systems"

        newentry['link'] = self.root_url + "/" + self.regime + "/" \
                           + self.regime_version + "/" +\
                           self.control_id + "/" + "maxlogins.xml"
        newentry['id'] = newentry['link']
        newentry['type'] = "application/xml"
        newentry['updated'] = self.time_updated
        newentry['summary'] = \
        "A list of the detected maximum number of allowable "\
        + "unsuccessful login attempts before account lockout" +\
        "per host indexed by IP address"

        newentry['author'] = [{'name':'Piston_CloudAudit', 'email':\
        'cloudaudit@pistoncloud.com'}]
        newentry['contributor'] = []

        self.entries.append(newentry)

    def get_manifest(self):
        if self.entries is None:
            self.get_evidence(None)

        xml_str = super(nist80053_ac7, self).get_manifest(None)

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
