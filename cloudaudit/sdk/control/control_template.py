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



from cloudaudit.evidence_engine import concurrent_sessions
import cloudaudit.api.ControlRegistry
import cloudaudit.control.entry
from time import gmtime, strftime


class CONTROL_TEMPLATE(cloudaudit.control.base.BaseControl):
    """
    INSERT CONTROL TITLE HERE

    INSERT_CONTROL_ID:

    DESCRIBE CONTROL HERE.
    """

    time_updated = "Never"
    evidence_gatherer = None # CUSTOMIZE
    control_title = "CUSTOMIZE_INSERT_TITLE"
    control_id = "CUSTOMIZE_INSERT_ID"
    control_subtitle = "CUSTOMIZE_INSERT_SUBTITLE"
    url_file = "CUSTOMIZE_INSERT_FILE" # usually this will be "manifest.xml"
    content = \
        "A list of the detected maximum number of allowable "\
        + "concurrent login sessions" +\
        "per host indexed by IP address"
    author_name = "John Doe"
    author_email = "jdoe@pistoncloud.com"
    content_title = "Concurrent Sessions Limitations"
    xml_root_tag = "maxConcurrentLogins"


    def __init__(self):
        super(self.__class__, self).__init__()
        self.xml_inventory = None
        self.evidence_data = None

    def get_evidence(self, req):
        if self.entries is None:
            self.entries = []

        super(CONTROL_TEMPLATE, self).get_evidence(req)

        if self.evidence_gatherer is None:
            self.evidence_gatherer = concurrent_sessions.ConcurrentSessionsLimit()

        self.evidence_data = self.evidence_gatherer.get_evidence()

        self.time_updated = strftime("%Y-%m-%d %H:%M:%S", gmtime())

        newentry = cloudaudit.control.entry.BaseEntry()

        newentry.title = self.__class__.content_title

        newlink = self.url + "/" + self.__class__.url_file

        
        newentry.link = newlink
        newentry.link_rel = "related"
        newentry.link_type = "xml"

        newentry.id = newlink

        newentry.updated = self.time_updated

        newentry.content = self.__class__.content

        newentry.add_author(self.__class__.author_name, self.__class__.author_email)

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

        xml_str = super(CONTROL_TEMPLATE, self).get_manifest(None)

        return xml_str

    def get_xml_inventory(self, req):
        if self.evidence_data is None:
            self.get_evidence(req)

        if self.evidence_data is None:
            self.evidence_data = {}

        return self.get_xml_inventory_base(req, self.evidence_data, self.__class__.xml_root_tag)
