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


def pam_login_deny(x):
    if 'deny' in x:
        return int(re.search('deny=(\d+)', x).groups()[0])


def od_login_deny(x):
    try:
        return int(re.search('^  *(\d+)', x).groups()[0])
    except AttributeError:
        return None


class MaxLoginAttempts(base.BaseEvidenceGatherer):
    def __init__(self, hosts=None):
        super(MaxLoginAttempts, self).__init__(ssh.SSHAccessor(hosts=hosts))

    def get_evidence(self):
        for host in super(MaxLoginAttempts, self).get_evidence():
            source = "PAM tally module"
            max_logins = self.accessor.execute('grep', 'tally', '/etc/*-auth',
                                               evaluator=pam_login_deny,
                                               hosts=[host])

            if not max_logins[0]:
                # PAM not defined?
                source = "faillog"
                max_logins = self.accessor.execute('od', '-x', '-s', '-j2',
                                                   '-N2', '/var/log/faillog',
                                                   evaluator=od_login_deny,
                                                   hosts=[host])
            if not max_logins[0]:
                max_logins[0] = 0
                source = "No enforcement mechanism."

            max_logins = {host: {'source': source,
                                 'max_logins': max_logins[0]}}
            self.evidence.update(max_logins)

        return self.evidence
