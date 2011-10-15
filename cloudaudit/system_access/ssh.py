# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2011 Piston Cloud Computing, Inc. All Rights Reserved.
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

import paramiko

from cloudaudit.system_access import base


class SSHAccessor(base.BaseAccessor):
    def __init__(self, private_key_file=None, hosts=None):
        super(self.__class__, self).__init__(hosts)

        self.os_map = {}
        self.private_key = private_key_file

        self.clients = dict([(host, self.get_client(host)) for host in hosts])

    def get_client(self, host, username='chris', private_key=None):
        # todo(chris): Implement caching as a decorator.

        if not private_key:
            private_key = self.private_key
        private_key = paramiko.RSAKey.from_private_key_file(private_key)

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, pkey=private_key, username=username)
        return client

    def execute(self, *command, **kwargs):
        evaluator = kwargs.get('evaluator', lambda x: x)
        hosts = kwargs.get('hosts', [])
        clients = kwargs.get('clients', self.clients)

        if hosts:
            clients = dict([(host, self.clients[host]) for host in hosts]) 

        command = str.join(' ', command)

        results = []
        for host, client in clients.items():
            try:
                stdin, stdout, stderr = client.exec_command(command)

                evaluated = [evaluator(l) for l in stdout.readlines()]
                evaluated = [x for x in evaluated if x is not None]
                if len(evaluated):
                    evaluated = evaluated[0]

                results.append(evaluated)
            except paramiko.SSHException, e:
                #self.log.warning(e)
                pass
        return results

    def get_operating_system(self, host):
        if not host in self.clients.keys():
            self.clients[host] = self.get_client(host)

        _os = self.os_map.get(host)
        if _os:
            return _os

        _os = self.execute('uname', evaluator=lambda x: x.strip(),
                                    clients={host: self.clients[host]})
        self.os_map[host] = _os
        return _os
