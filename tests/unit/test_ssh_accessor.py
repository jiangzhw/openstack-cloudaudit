import os
import StringIO
import unittest2

from cloudaudit.system_access import ssh


class FakeParamikoSSHClient(object):
    expected = ('stdin', StringIO.StringIO('FAKE'), 'stdout')

    def set_missing_host_key_policy(self, policy):
        pass

    def connect(self, *args, **kwargs):
        pass

    def exec_command(self, *args, **kwargs):
        return self.expected

class TestSSHAccessor(unittest2.TestCase):
    def setUp(self):
        self.old_client = ssh.paramiko.SSHClient
        ssh.paramiko.SSHClient = FakeParamikoSSHClient

    def tearDown(self):
        ssh.paramiko.SSHClient = self.old_client

    def test_ssh_accessor_without_a_keyfile_should_raise(self):
        self.assertRaises(ssh.paramiko.SSHException,
                          ssh.SSHAccessor, hosts=['testa', 'testb'])

    def test_execute(self):
        ssh_client = ssh.SSHAccessor(
                          private_key_file=os.path.expanduser('~/.ssh/id_rsa'),
                          hosts=['testa', 'testb'])

        for host, client in ssh_client.clients.items():
            exp = StringIO.StringIO('THIS IS JUST A FAKE STRING')
            client.expected = ('stdin', exp, 'stdout')

        self.assertEqual(['THIS IS JUST A FAKE STRING', 
                          'THIS IS JUST A FAKE STRING'],
                          ssh_client.execute('echo', 'THIS', 'IS', 'JUST', 'A',
                                             'FAKE', 'STRING'))

    def test_execute_with_raise_should_pass(self):
        ssh_client = ssh.SSHAccessor(
                          private_key_file=os.path.expanduser('~/.ssh/id_rsa'),
                          hosts=['testa', 'testb'])

        for host, client in ssh_client.clients.items():
            exp = StringIO.StringIO('THIS IS JUST A FAKE STRING')
            client.expected = ('stdin', exp, 'stdout')

            if host == 'testb':
                def fake_exec_with_explosions(self, *args, **kwargs):
                    raise ssh.paramiko.SSHException("foo")

                client.exec_command = fake_exec_with_explosions

        self.assertEqual(['THIS IS JUST A FAKE STRING'],
                          ssh_client.execute('echo', 'THIS', 'IS', 'JUST', 'A',
                                             'FAKE', 'STRING'))

    def test_get_operating_system(self):
        ssh_client = ssh.SSHAccessor(
                          private_key_file=os.path.expanduser('~/.ssh/id_rsa'),
                          hosts=['testa', 'testb'])

        for host, client in ssh_client.clients.items():
            exp = StringIO.StringIO('Linux')
            client.expected = ('stdin', exp, 'stdout')
        
        self.assertEqual(['Linux'], ssh_client.get_operating_system(host='testa'))
        self.assertEqual(['Linux'], ssh_client.get_operating_system(host='testa'))
        self.assertEqual(['Linux'], ssh_client.get_operating_system(host='testb'))
        self.assertEqual(['FAKE'],
                         ssh_client.get_operating_system(host='testc'))

#    def test_getAllServers(self):
#        myList = self.accessor.getAllSshSystems()
#
#        for server in myList:
#            server_ip = server.addresses['private']
#
#            if len(server_ip) > 0:
#                ourClient = self.accessor.getSshClient(server_ip[0], "nokeyhere", "")
#                o_stdin, o_stdout, o_stderr = self.accessor.runSshCommnad(ourClient, "ls -l /tmp")
#                line = o_stdout.readline()
#                self.assertRegexpMatches(line, "total")
#
#        osMap = self.accessor.getOS(myList)
#
#        self.assertTrue(len(myList) > 0)
