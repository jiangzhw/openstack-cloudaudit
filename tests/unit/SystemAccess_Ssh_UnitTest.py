__author__ = 'joshd'


import random
import unittest
import cloudaudit.SystemAccess_Ssh

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.seq = range(10)
        self.accessor = cloudaudit.SystemAccess_Ssh.SystemAccess_Ssh()
 #       self.accessor = cloudaudit.SystemAccess_Ssh()


    def test_getAllServers(self):
        myList = self.accessor.getAllSshSystems()

        for server in myList:
            server_ip = server.addresses['private']

            if len(server_ip) > 0:
                ourClient = self.accessor.getSshClient(server_ip[0], "nokeyhere", "")
                o_stdin, o_stdout, o_stderr = self.accessor.runSshCommnad(ourClient, "ls -l /tmp")
                line = o_stdout.readline()
                self.assertRegexpMatches(line, "total")

        osMap = self.accessor.getOS(myList)

        self.assertTrue(len(myList) > 0)
