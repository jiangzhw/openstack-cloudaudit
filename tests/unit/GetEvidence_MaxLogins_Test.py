__author__ = 'joshd'

import random
import unittest
import cloudaudit.SystemAccess_Ssh
import cloudaudit.api.Evidence_MaxLoginAttempts

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.seq = range(10)
        self.gatherer = cloudaudit.api.Evidence_MaxLoginAttempts.Evidence_MaxLoginAttempts()


    def test_getEvidence(self):
        myList = self.gatherer.getSystems()

        maxLoginResults = self.gatherer.getEvidence()


        self.assertTrue(len(myList) > 0)
