"""
Test case for BikeshareStationStatus
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from tokyo_docomo_bikeshare_producer_data.bikesharestationstatus import BikeshareStationStatus


class Test_BikeshareStationStatus(unittest.TestCase):
    """
    Test case for BikeshareStationStatus
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_BikeshareStationStatus.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of BikeshareStationStatus for testing
        """
        instance = BikeshareStationStatus(
            system_id='laqzylwlzzoxqwklpcin',
            station_id='akmjxhsnfdterppdmhoy',
            num_bikes_available=int(21),
            num_bikes_disabled=int(84),
            num_docks_available=int(92),
            num_docks_disabled=int(97),
            is_installed=True,
            is_renting=True,
            is_returning=False,
            last_reported=int(90)
        )
        return instance

    
    def test_system_id_property(self):
        """
        Test system_id property
        """
        test_value = 'laqzylwlzzoxqwklpcin'
        self.instance.system_id = test_value
        self.assertEqual(self.instance.system_id, test_value)
    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'akmjxhsnfdterppdmhoy'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_num_bikes_available_property(self):
        """
        Test num_bikes_available property
        """
        test_value = int(21)
        self.instance.num_bikes_available = test_value
        self.assertEqual(self.instance.num_bikes_available, test_value)
    
    def test_num_bikes_disabled_property(self):
        """
        Test num_bikes_disabled property
        """
        test_value = int(84)
        self.instance.num_bikes_disabled = test_value
        self.assertEqual(self.instance.num_bikes_disabled, test_value)
    
    def test_num_docks_available_property(self):
        """
        Test num_docks_available property
        """
        test_value = int(92)
        self.instance.num_docks_available = test_value
        self.assertEqual(self.instance.num_docks_available, test_value)
    
    def test_num_docks_disabled_property(self):
        """
        Test num_docks_disabled property
        """
        test_value = int(97)
        self.instance.num_docks_disabled = test_value
        self.assertEqual(self.instance.num_docks_disabled, test_value)
    
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
        test_value = True
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
        test_value = int(90)
        self.instance.last_reported = test_value
        self.assertEqual(self.instance.last_reported, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = BikeshareStationStatus.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = BikeshareStationStatus.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

