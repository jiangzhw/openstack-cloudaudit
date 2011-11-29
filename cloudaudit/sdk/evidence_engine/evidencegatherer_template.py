#
# Copyright 2011, Piston Cloud Computing, Inc.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import re

from cloudaudit.evidence_engine import base
from cloudaudit.system_access import ssh


def content_search_helper(x):
    content_search = "CUSTOMIZE_CONTENT_TO_SEARCH"
    if content_search in x:
        return int(re.search(content_search + '\s+(\w+)', x).groups()[0])


class EvidenceGatherer_Template(base.BaseEvidenceGatherer):

    source_1 = "Sshd Configuration"
    command_1 = "grep tally /etc/ssh/sshd_config"
    manifest_xml_tag = "concurrent_sessions_limitation"

    def __init__(self, hosts=None):
        super(ConcurrentSessionsLimit, self).\
        __init__(ssh.SSHAccessor(hosts=hosts))

    def get_evidence(self):
        for host in super(ConcurrentSessionsLimit, self).get_evidence():
            source = self.__class__.source_1
            concurrent_sessions = \
            self.accessor.execute(self.__class__.command_1,
                                    evaluator=content_search_helper,
                                    hosts=[host])
            if concurrent_sessions is None:
                enabled = Fales
            else:
                enabled = True

            return_values = {host: {'source': source,
                                 self.__class__.manifest_xml_tag: enabled}}
            self.evidence.update(return_values)

        return self.evidence
