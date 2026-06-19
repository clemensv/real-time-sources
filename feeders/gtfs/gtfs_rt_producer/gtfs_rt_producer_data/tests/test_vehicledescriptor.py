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
            id='tocgcaydypxdavqxoexc',
            label='mymttbucskzpmywgvdeo',
            license_plate='sysmlnhuatfzdktmaixi'
        )
        return instance

    
    def test_id_property(self):
        """
        Test id property
        """
        test_value = 'tocgcaydypxdavqxoexc'
        self.instance.id = test_value
        self.assertEqual(self.instance.id, test_value)
    
    def test_label_property(self):
        """
        Test label property
        """
        test_value = 'mymttbucskzpmywgvdeo'
        self.instance.label = test_value
        self.assertEqual(self.instance.label, test_value)
    
    def test_license_plate_property(self):
        """
        Test license_plate property
        """
        test_value = 'sysmlnhuatfzdktmaixi'
        self.instance.license_plate = test_value
        self.assertEqual(self.instance.license_plate, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = VehicleDescriptor.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = VehicleDescriptor.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

