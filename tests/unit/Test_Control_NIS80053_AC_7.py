__author__ = 'joshd'

import random
import unittest
import cloudaudit.SystemAccess_Ssh
import cloudaudit.api.Evidence_MaxLoginAttempts
import cloudaudit.api.Control_Nist800_53_AC_7

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.seq = range(10)
        self.control = cloudaudit.api.Control_Nist800_53_AC_7.Control_Nist800_53_AC_7()


    def test_getEvidence(self):
        myXml = self.control.getManifest()

        myXml = self.control.getResponse(None)

        print myXml

        newXml = self.control.getXmlInventory(None)

        print newXml

        self.assertTrue(len(myXml) > 0)
