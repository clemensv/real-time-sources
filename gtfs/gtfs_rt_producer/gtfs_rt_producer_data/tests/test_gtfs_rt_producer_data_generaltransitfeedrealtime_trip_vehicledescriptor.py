"""
Test case for VehicleDescriptor
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedrealtime.trip.vehicledescriptor import VehicleDescriptor


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
            id='dxncxalbyxmegerhfjnx',
            label='zzdbzrmfwvhwsfknsyxz',
            license_plate='itasharctcyfnpeqevct'
        )
        return instance

    
    def test_id_property(self):
        """
        Test id property
        """
        test_value = 'dxncxalbyxmegerhfjnx'
        self.instance.id = test_value
        self.assertEqual(self.instance.id, test_value)
    
    def test_label_property(self):
        """
        Test label property
        """
        test_value = 'zzdbzrmfwvhwsfknsyxz'
        self.instance.label = test_value
        self.assertEqual(self.instance.label, test_value)
    
    def test_license_plate_property(self):
        """
        Test license_plate property
        """
        test_value = 'itasharctcyfnpeqevct'
        self.instance.license_plate = test_value
        self.assertEqual(self.instance.license_plate, test_value)
    
