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


def idle_session_screenlock(x):
    if 'true' in x:
        return true
    else:
        return false

class ConcurrentSessionsLimit(base.BaseEvidenceGatherer):
    def __init__(self, hosts=None):
        super(LastLoginNotification, self).\
        __init__(ssh.SSHAccessor(hosts=hosts))

    def get_eivdence(self):
        for host in super(LastLoginNotification, self).get_evidence():
            source = "Sshd Configuration"
            idle_lock = \
            self.accessor.execute('gconftool', '--get',
                    '/apps/gnome-screensaver/idle_activation_enabled',
                                    evaluator=concurrent_sessions_limit,
                                    hosts=[host])
            
            return_values = {host: {'source': source,
                                 'idle_lock': idle_lock}}
            self.evidence.update(return_values)

        return self.evidence
