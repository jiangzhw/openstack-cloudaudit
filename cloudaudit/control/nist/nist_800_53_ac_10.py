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


from time import gmtime, strftime
from cloudaudit.control import nist
from cloudaudit.evidence_engine import concurrent_sessions
import cloudaudit.api.ControlRegistry
import cloudaudit.control.entry


class NIST_800_53_ac10(nist.NIST_800_53_Control):
    """
    Control evidence gathering implementation for NIST 800-53 control AC-10

    AC-10:

    Control:  The information system limits the number of concurrent sessions
    for each system account to [Assignment: organization-defined number].
    Supplemental Guidance:  The organization may define the maximum number
    of concurrent sessions for an information system account globally, by
    account type, by account, or a combination.  This control addresses
    concurrent sessions for a given information system account and does not
    address concurrent sessions by a single user via multiple system accounts.
    """

    time_updated = "Never"
    evidence_gatherer = None
    control_title = "NIS 800-53 AC-10 Concurrent Session Control"
    control_id = "ac/10"
    control_subtitle = "Concurrent Session Control"

    def __init__(self):
        super(self.__class__, self).__init__()
        self.xml_inventory = None
        self.evidence_data = None

    def get_evidence(self, req):
        if self.entries is None:
            self.entries = []

        super(NIST_800_53_ac10, self).get_evidence(req)

        if self.evidence_gatherer is None:
            self.evidence_gatherer = concurrent_sessions.ConcurrentSessionsLimit()

        self.evidence_data = self.evidence_gatherer.get_evidence()

        self.time_updated = strftime("%Y-%m-%d %H:%M:%S", gmtime())


        newentry = cloudaudit.control.entry.BaseEntry()

        newentry.title = \
        "Concurrent Sessions Limitations"

        newlink = self.url + "/" + "concurrentsessions.xml"
        newentry.link = newlink
        newentry.link_rel = "related"
        newentry.link_type = "xml"

        newentry.id = newlink

        newentry.updated = self.time_updated

        newentry.content = \
        "A list of the detected maximum number of allowable "\
        + "concurrent login sessions" +\
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

        xml_str = super(NIST_800_53_ac10, self).get_manifest(None)

        return xml_str

    def get_xml_inventory(self, req):
        if self.evidence_data is None:
            self.get_evidence(req)

        if self.evidence_data is None:
            self.evidence_data = {}

        return self.get_xml_inventory_base(req, self.evidence_data, "maxConcurrentLogins")
