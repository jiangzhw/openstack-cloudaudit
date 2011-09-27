__author__ = 'joshd'


import random
import unittest
import cloudaudit.api.ControlRegistry

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.seq = range(10)
        self.controlreg = cloudaudit.api.ControlRegistry.ControlRegistry()


    def test_getControl(self):

        control = self.controlreg.getControlFromUrl("gov/nist/crc/sp800-53/r3/ac/7/adsf")
        self.assertTrue(control != None)
