"""
Test case for VehicleDescriptor
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeed.tripupdate.vehicledescriptor import VehicleDescriptor

class Test_VehicleDescriptor(unittest.TestCase):
    """
    Test case for VehicleDescriptor
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_VehicleDescriptor.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of VehicleDescriptor for testing
        """
        instance = VehicleDescriptor(
            id='pparvumwaepcxfkpoljo',
            label='wbdgtwkcgccxitdpavor',
            license_plate='pfpyldhgesgbdfzqxdao'
        )
        return instance

    
    def test_id_property(self):
        """
        Test id property
        """
        test_value = 'pparvumwaepcxfkpoljo'
        self.instance.id = test_value
        self.assertEqual(self.instance.id, test_value)
    
    def test_label_property(self):
        """
        Test label property
        """
        test_value = 'wbdgtwkcgccxitdpavor'
        self.instance.label = test_value
        self.assertEqual(self.instance.label, test_value)
    
    def test_license_plate_property(self):
        """
        Test license_plate property
        """
        test_value = 'pfpyldhgesgbdfzqxdao'
        self.instance.license_plate = test_value
        self.assertEqual(self.instance.license_plate, test_value)
    
