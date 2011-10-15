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

import StringIO
import unittest2

from cloudaudit.system_access import ssh
from cloudaudit.evidence_engine import max_login_attempts


class FakeRSAKey(object):
    @staticmethod
    def from_private_key_file(blah):
        blah


class FakeParamikoSSHClient(object):
    expected = ('stdin', StringIO.StringIO('fake'), 'stdout')

    def set_missing_host_key_policy(self, policy):
        pass

    def connect(self, *args, **kwargs):
        pass

    def exec_command(self, *args, **kwargs):
        self.expected[1].seek(0)
        return self.expected


class TestMaxLoginAttempts(unittest2.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.hosts = ['host1', 'host2', 'host3']
        self.old_client = ssh.paramiko.SSHClient
        self.old_paramiko_rsakey = ssh.paramiko.RSAKey

        ssh.paramiko.RSAKey = FakeRSAKey
        ssh.paramiko.SSHClient = FakeParamikoSSHClient

    def tearDown(self):
        ssh.paramiko.SSHClient = self.old_client
        ssh.paramiko.RSAKey = self.old_paramiko_rsakey

    def test_max_login_attempts_with_pam(self):
        pam_string = StringIO.StringIO(
                        "auth required pam_tally.so no_magic_root\n"
                        "account required pam_tally.so deny=3 no_magic_root lock_time=180")

        FakeParamikoSSHClient.expected = ('s', pam_string, 'se')

        max_attempts = max_login_attempts.MaxLoginAttempts(self.hosts)

        expected = {'host3': {'source': 'PAM tally module', 'max_logins': 3},
                    'host2': {'source': 'PAM tally module', 'max_logins': 3},
                    'host1': {'source': 'PAM tally module', 'max_logins': 3}}

        self.assertEqual(expected, max_attempts.get_evidence())

    def test_max_login_attempts_with_od(self):
        od_string = StringIO.StringIO("0000002   0003\n"
                                      "             3\n"
                                      "0000004")

        FakeParamikoSSHClient.expected = ('s', od_string, 'se')

        max_attempts = max_login_attempts.MaxLoginAttempts(self.hosts)
        expected = {'host3': {'source': 'faillog', 'max_logins': 3},
                    'host2': {'source': 'faillog', 'max_logins': 3},
                    'host1': {'source': 'faillog', 'max_logins': 3}}

        self.assertEqual(expected, max_attempts.get_evidence())

    def test_max_login_attempts_with_no_enforcement(self):
        no_enforcement_string = StringIO.StringIO("")
        FakeParamikoSSHClient.expected = ('s', no_enforcement_string, 'se')

        max_attempts = max_login_attempts.MaxLoginAttempts(self.hosts)
        expected = {'host3': {'source': 'No enforcement mechanism.', 
                              'max_logins': 0},
                    'host2': {'source': 'No enforcement mechanism.',
                              'max_logins': 0},
                    'host1': {'source': 'No enforcement mechanism.',
                              'max_logins': 0}}

        self.assertEqual(expected, max_attempts.get_evidence())
