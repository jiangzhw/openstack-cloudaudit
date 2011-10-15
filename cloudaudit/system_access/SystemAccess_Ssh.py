

__author__ = 'joshd'


import novaclient
import paramiko
import libssh2
import cmd
import types


class system_access_ssh(object):

    """
    A controller that produces information on the Glance API versions.
    """

    def __init__(self):
        self.openstackclient = None
        self.clients = {}
        self.osmap = {}

    def get_all_ssh_systems(self):
        self.openstackclient = \
            novaclient.OpenStack("joshd",
                                 "f82d944c-84f7-4a60-8f61-f0ca4b54f860",
                                 "http://127.0.0.1:8774/v1.0/")

        list = self.openstackclient.images.list()

        list = self.openstackclient.servers.list()

        newlist = []

        for server in list:
            if len(server.addresses['private']) > 0:
                newlist.append(server)

        list = []

        for server in newlist:
            self.test_ssh(server.addresses['private'][0], "", "")

        return newlist

    def test_ssh(self, ip, key, password):

        myclient = self.get_ssh_client(ip, key, password)
        if myclient == None:
            return False

        return True

    def get_ssh_client(self, ip, key, password):

        if ip in self.clients:
            return self.clients[ip]

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # XXX TODO:  don't hardcode this
        privatekeyfile = "/home/joshd/NOVACREDS/privkey"
        mykey = paramiko.RSAKey.from_private_key_file(privatekeyfile)
        public_host_key = paramiko.RSAKey(data=str(mykey))
        client.connect(ip, pkey=mykey, username="ubuntu")

        self.clients[ip] = client

        return client

    def run_ssh_commnad(self, client, command):
        o_stdin, o_stdout, o_stderr = client.exec_command(command)

        return o_stdin, o_stdout, o_stderr

    def get_os(self, server):
        servers = []
        retvals = {}
        if isinstance(server, types.ListType):
            for srv in server:
                if len(srv.addresses['private']) > 0:
                    servers.append(srv.addresses['private'][0])
        else:
            servers = [server.addresses['private'][0]]

        for srv in servers:

            if srv in self.osmap:
                retvals[srv] = self.osmap[srv]
                continue

            lines = self.get_command_output(srv, "uname")
            if len(lines) > 0:
                self.osmap[srv] = lines[0].strip()
                retvals[srv] = lines[0].strip()

        return retvals

    def get_command_output(self, ip, command):

        client = self.get_ssh_client(ip, "", "")

        o_stdin, o_stdout, o_stderr = self.run_ssh_commnad(client, command)

        lines = o_stdout.readlines()

        return lines
