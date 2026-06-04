"""
Test case for StationStatus
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gbfs_bikeshare_amqp_producer_data.stationstatus import StationStatus


class Test_StationStatus(unittest.TestCase):
    """
    Test case for StationStatus
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_StationStatus.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of StationStatus for testing
        """
        instance = StationStatus(
            system_id='dljhaznqqvuqfrmpmcdy',
            station_id='fgulrufmcyigbnvojyey',
            num_bikes_available=int(60),
            num_docks_available=int(100),
            num_ebikes_available=int(89),
            is_installed=True,
            is_renting=False,
            is_returning=False,
            last_reported=int(48)
        )
        return instance

    
    def test_system_id_property(self):
        """
        Test system_id property
        """
        test_value = 'dljhaznqqvuqfrmpmcdy'
        self.instance.system_id = test_value
        self.assertEqual(self.instance.system_id, test_value)
    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'fgulrufmcyigbnvojyey'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_num_bikes_available_property(self):
        """
        Test num_bikes_available property
        """
        test_value = int(60)
        self.instance.num_bikes_available = test_value
        self.assertEqual(self.instance.num_bikes_available, test_value)
    
    def test_num_docks_available_property(self):
        """
        Test num_docks_available property
        """
        test_value = int(100)
        self.instance.num_docks_available = test_value
        self.assertEqual(self.instance.num_docks_available, test_value)
    
    def test_num_ebikes_available_property(self):
        """
        Test num_ebikes_available property
        """
        test_value = int(89)
        self.instance.num_ebikes_available = test_value
        self.assertEqual(self.instance.num_ebikes_available, test_value)
    
    def test_is_installed_property(self):
        """
        Test is_installed property
        """
        test_value = True
        self.instance.is_installed = test_value
        self.assertEqual(self.instance.is_installed, test_value)
    
    def test_is_renting_property(self):
        """
        Test is_renting property
        """
        test_value = False
        self.instance.is_renting = test_value
        self.assertEqual(self.instance.is_renting, test_value)
    
    def test_is_returning_property(self):
        """
        Test is_returning property
        """
        test_value = False
        self.instance.is_returning = test_value
        self.assertEqual(self.instance.is_returning, test_value)
    
    def test_last_reported_property(self):
        """
        Test last_reported property
        """
        test_value = int(48)
        self.instance.last_reported = test_value
        self.assertEqual(self.instance.last_reported, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = StationStatus.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = StationStatus.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

