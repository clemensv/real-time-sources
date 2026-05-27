"""
Test case for WeatherStation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from geosphere_austria_producer_data.at.geosphere.tawes.weatherstation import WeatherStation


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
            station_id='xjekxnzvfeunpuoiytmc',
            station_name='nogkqkiodboyauyakxhk',
            latitude=float(26.953820142771335),
            longitude=float(93.78988059324853),
            altitude=float(89.28887825206517),
            state='eolgnyibdoirunvoobrn'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'xjekxnzvfeunpuoiytmc'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'nogkqkiodboyauyakxhk'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(26.953820142771335)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(93.78988059324853)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_altitude_property(self):
        """
        Test altitude property
        """
        test_value = float(89.28887825206517)
        self.instance.altitude = test_value
        self.assertEqual(self.instance.altitude, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'eolgnyibdoirunvoobrn'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = WeatherStation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
