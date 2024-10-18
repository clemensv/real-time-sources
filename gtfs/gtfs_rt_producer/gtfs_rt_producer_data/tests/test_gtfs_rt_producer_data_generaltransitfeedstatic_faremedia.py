"""
Test case for FareMedia
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedstatic.faremedia import FareMedia


class Test_FareMedia(unittest.TestCase):
    """
    Test case for FareMedia
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_FareMedia.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of FareMedia for testing
        """
        instance = FareMedia(
            fareMediaId='uqfqwzswelgljkeiaeqy',
            fareMediaName='kmyhoclulkpfxlfudmll',
            fareMediaDesc='aubpwvyfdodmwqfuswka',
            fareMediaUrl='plairefhaauxzrcgnden'
        )
        return instance

    
    def test_fareMediaId_property(self):
        """
        Test fareMediaId property
        """
        test_value = 'uqfqwzswelgljkeiaeqy'
        self.instance.fareMediaId = test_value
        self.assertEqual(self.instance.fareMediaId, test_value)
    
    def test_fareMediaName_property(self):
        """
        Test fareMediaName property
        """
        test_value = 'kmyhoclulkpfxlfudmll'
        self.instance.fareMediaName = test_value
        self.assertEqual(self.instance.fareMediaName, test_value)
    
    def test_fareMediaDesc_property(self):
        """
        Test fareMediaDesc property
        """
        test_value = 'aubpwvyfdodmwqfuswka'
        self.instance.fareMediaDesc = test_value
        self.assertEqual(self.instance.fareMediaDesc, test_value)
    
    def test_fareMediaUrl_property(self):
        """
        Test fareMediaUrl property
        """
        test_value = 'plairefhaauxzrcgnden'
        self.instance.fareMediaUrl = test_value
        self.assertEqual(self.instance.fareMediaUrl, test_value)
    
