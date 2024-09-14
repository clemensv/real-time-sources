"""
Test case for FareRules
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedstatic.farerules import FareRules

class Test_FareRules(unittest.TestCase):
    """
    Test case for FareRules
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_FareRules.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of FareRules for testing
        """
        instance = FareRules(
            fareId='hpfeixiqgzfeowneeazy',
            routeId='msnciutungtnojoncedy',
            originId='izpgwjqawjbslkddizoo',
            destinationId='jisfrzhkgnxukxcjmmnc',
            containsId='rigakabkirfeueffcdjw'
        )
        return instance

    
    def test_fareId_property(self):
        """
        Test fareId property
        """
        test_value = 'hpfeixiqgzfeowneeazy'
        self.instance.fareId = test_value
        self.assertEqual(self.instance.fareId, test_value)
    
    def test_routeId_property(self):
        """
        Test routeId property
        """
        test_value = 'msnciutungtnojoncedy'
        self.instance.routeId = test_value
        self.assertEqual(self.instance.routeId, test_value)
    
    def test_originId_property(self):
        """
        Test originId property
        """
        test_value = 'izpgwjqawjbslkddizoo'
        self.instance.originId = test_value
        self.assertEqual(self.instance.originId, test_value)
    
    def test_destinationId_property(self):
        """
        Test destinationId property
        """
        test_value = 'jisfrzhkgnxukxcjmmnc'
        self.instance.destinationId = test_value
        self.assertEqual(self.instance.destinationId, test_value)
    
    def test_containsId_property(self):
        """
        Test containsId property
        """
        test_value = 'rigakabkirfeueffcdjw'
        self.instance.containsId = test_value
        self.assertEqual(self.instance.containsId, test_value)
    
