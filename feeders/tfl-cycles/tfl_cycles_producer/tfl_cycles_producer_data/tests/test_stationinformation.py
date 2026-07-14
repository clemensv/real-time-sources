"""
Test case for StationInformation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from tfl_cycles_producer_data.stationinformation import StationInformation
import datetime


class Test_StationInformation(unittest.TestCase):
    """
    Test case for StationInformation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_StationInformation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of StationInformation for testing
        """
        instance = StationInformation(
            station_id='xzkqldawuhiwmgnxskux',
            name='yatdxknuainwuambrlxw',
            lat=float(64.88626578415838),
            lon=float(16.173602686187838),
            terminal_name='pygkeuilssbfcwonirha',
            capacity=int(73),
            temporary=True,
            install_date=datetime.datetime.now(datetime.timezone.utc),
            removal_date=datetime.datetime.now(datetime.timezone.utc)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'xzkqldawuhiwmgnxskux'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'yatdxknuainwuambrlxw'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_lat_property(self):
        """
        Test lat property
        """
        test_value = float(64.88626578415838)
        self.instance.lat = test_value
        self.assertEqual(self.instance.lat, test_value)
    
    def test_lon_property(self):
        """
        Test lon property
        """
        test_value = float(16.173602686187838)
        self.instance.lon = test_value
        self.assertEqual(self.instance.lon, test_value)
    
    def test_terminal_name_property(self):
        """
        Test terminal_name property
        """
        test_value = 'pygkeuilssbfcwonirha'
        self.instance.terminal_name = test_value
        self.assertEqual(self.instance.terminal_name, test_value)
    
    def test_capacity_property(self):
        """
        Test capacity property
        """
        test_value = int(73)
        self.instance.capacity = test_value
        self.assertEqual(self.instance.capacity, test_value)
    
    def test_temporary_property(self):
        """
        Test temporary property
        """
        test_value = True
        self.instance.temporary = test_value
        self.assertEqual(self.instance.temporary, test_value)
    
    def test_install_date_property(self):
        """
        Test install_date property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.install_date = test_value
        self.assertEqual(self.instance.install_date, test_value)
    
    def test_removal_date_property(self):
        """
        Test removal_date property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.removal_date = test_value
        self.assertEqual(self.instance.removal_date, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = StationInformation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = StationInformation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

