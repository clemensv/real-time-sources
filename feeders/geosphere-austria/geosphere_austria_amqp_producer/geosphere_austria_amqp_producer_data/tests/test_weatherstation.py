"""
Test case for WeatherStation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from geosphere_austria_amqp_producer_data.at.geosphere.tawes.weatherstation import WeatherStation


class Test_WeatherStation(unittest.TestCase):
    """
    Test case for WeatherStation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_WeatherStation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of WeatherStation for testing
        """
        instance = WeatherStation(
            station_id='vzaqfcdjqfpmuuhiqsea',
            station_name='ctvzkvjsodrmguqmigyl',
            latitude=float(2.6875437349347497),
            longitude=float(65.84092468497522),
            altitude=float(95.42264380479553),
            state='fbdwitcclyukhcylxgik'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'vzaqfcdjqfpmuuhiqsea'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'ctvzkvjsodrmguqmigyl'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(2.6875437349347497)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(65.84092468497522)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_altitude_property(self):
        """
        Test altitude property
        """
        test_value = float(95.42264380479553)
        self.instance.altitude = test_value
        self.assertEqual(self.instance.altitude, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'fbdwitcclyukhcylxgik'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = WeatherStation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = WeatherStation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

