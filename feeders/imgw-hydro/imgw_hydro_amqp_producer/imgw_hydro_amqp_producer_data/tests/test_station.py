"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from imgw_hydro_amqp_producer_data.station import Station


class Test_Station(unittest.TestCase):
    """
    Test case for Station
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Station.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Station for testing
        """
        instance = Station(
            station_id='oorgfrwkpxjcsqvgeeqw',
            station_name='wwoqgrpyattyhwdwoqfl',
            river='ktamummyfryvkxlgnagk',
            voivodeship='pssztgzuypurjjvhftov',
            longitude=float(56.858835112804115),
            latitude=float(89.63377418520159),
            basin='rvnjwdkjlkioigoxvwii'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'oorgfrwkpxjcsqvgeeqw'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'wwoqgrpyattyhwdwoqfl'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_river_property(self):
        """
        Test river property
        """
        test_value = 'ktamummyfryvkxlgnagk'
        self.instance.river = test_value
        self.assertEqual(self.instance.river, test_value)
    
    def test_voivodeship_property(self):
        """
        Test voivodeship property
        """
        test_value = 'pssztgzuypurjjvhftov'
        self.instance.voivodeship = test_value
        self.assertEqual(self.instance.voivodeship, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(56.858835112804115)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(89.63377418520159)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_basin_property(self):
        """
        Test basin property
        """
        test_value = 'rvnjwdkjlkioigoxvwii'
        self.instance.basin = test_value
        self.assertEqual(self.instance.basin, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Station.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Station.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

