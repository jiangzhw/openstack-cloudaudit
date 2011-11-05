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

from cloudaudit.control import nist
from cloudaudit.evidence_engine import max_login_attempts
import cloudaudit.control.entry
from lxml.builder import E
from lxml import etree
from webob import Response
import webob


class NIST_800_53_ac7(nist.NIST_800_53_Control):
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

    time_updated = "Never"
    control_title = "NIS 800-53 AC-7 Maximum Unsuccessful Logins"
    control_id = "ac/7"
    control_subtitle = "Max Unsuccessful Logins before Lockout"

    def __init__(self):
        super(self.__class__, self).__init__()
        self.xml_inventory = None
        self.max_logins = None
        self.evidence_gatherer = None

    def get_evidence(self, req):
        if self.entries is None:
            self.entries = []

        super(NIST_800_53_ac7, self).get_evidence(req)

        if self.evidence_gatherer is None:
            self.evidence_gatherer = max_login_attempts.MaxLoginAttempts()

        self.max_logins = self.evidence_gatherer.get_evidence()

        self.time_updated = "2010-01-13T18:30:02Z"

        newentry = cloudaudit.control.entry.BaseEntry()

        newentry.title = \
        "Maximum Unsuccessful Logins Inventory for all Unix systems"

        newlink = self.url + "/" + "maxlogins.xml"
        newentry.link = newlink
        newentry.link_rel = "related"
        newentry.link_type = "xml"

        newentry.id = newlink

        newentry.updated = self.time_updated

        newentry.content = \
        "A list of the detected maximum number of allowable "\
        + "unsuccessful login attempts before account lockout" +\
        "per host indexed by IP address"

        newentry.add_author("John Doe", "jdoe@pistoncc.com")

        self.entries.append(newentry)

    def process_request(self, req):
        resp = super(self.__class__, self).process_request(req)

        if resp is None:
            return self.get_xml_inventory(req)
        else:
            return resp


    def get_manifest(self, req):
        if self.entries is None:
            self.get_evidence(None)

        xml_str = super(NIST_800_53_ac7, self).get_manifest(req)

        return xml_str

    def get_xml_inventory(self, req):
        if self.max_logins is None:
            self.max_logins = self.get_evidence(req)

        if self.max_logins is None:
            self.max_logins = {}

        return self.get_xml_inventory_base(req, self.max_logins, "maxUnsuccessfulLogins")
