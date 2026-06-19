"""
Test case for SensorInfo
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from sensor_community_producer_data.io.sensor.community.sensorinfo import SensorInfo


class Test_SensorInfo(unittest.TestCase):
    """
    Test case for SensorInfo
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_SensorInfo.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of SensorInfo for testing
        """
        instance = SensorInfo(
            sensor_id=int(24),
            sensor_type_id=int(83),
            sensor_type_name='ufneffuosszyujwlsgsi',
            sensor_type_manufacturer='sxewueuggjcjwcxnkkkk',
            pin='trbdeskiuktpbpxqewph',
            location_id=int(20),
            latitude=float(27.318038751801875),
            longitude=float(88.9905322877415),
            altitude=float(28.07074346007529),
            country='ilbbksbqspxohhfwmoji',
            indoor=True
        )
        return instance

    
    def test_sensor_id_property(self):
        """
        Test sensor_id property
        """
        test_value = int(24)
        self.instance.sensor_id = test_value
        self.assertEqual(self.instance.sensor_id, test_value)
    
    def test_sensor_type_id_property(self):
        """
        Test sensor_type_id property
        """
        test_value = int(83)
        self.instance.sensor_type_id = test_value
        self.assertEqual(self.instance.sensor_type_id, test_value)
    
    def test_sensor_type_name_property(self):
        """
        Test sensor_type_name property
        """
        test_value = 'ufneffuosszyujwlsgsi'
        self.instance.sensor_type_name = test_value
        self.assertEqual(self.instance.sensor_type_name, test_value)
    
    def test_sensor_type_manufacturer_property(self):
        """
        Test sensor_type_manufacturer property
        """
        test_value = 'sxewueuggjcjwcxnkkkk'
        self.instance.sensor_type_manufacturer = test_value
        self.assertEqual(self.instance.sensor_type_manufacturer, test_value)
    
    def test_pin_property(self):
        """
        Test pin property
        """
        test_value = 'trbdeskiuktpbpxqewph'
        self.instance.pin = test_value
        self.assertEqual(self.instance.pin, test_value)
    
    def test_location_id_property(self):
        """
        Test location_id property
        """
        test_value = int(20)
        self.instance.location_id = test_value
        self.assertEqual(self.instance.location_id, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(27.318038751801875)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(88.9905322877415)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_altitude_property(self):
        """
        Test altitude property
        """
        test_value = float(28.07074346007529)
        self.instance.altitude = test_value
        self.assertEqual(self.instance.altitude, test_value)
    
    def test_country_property(self):
        """
        Test country property
        """
        test_value = 'ilbbksbqspxohhfwmoji'
        self.instance.country = test_value
        self.assertEqual(self.instance.country, test_value)
    
    def test_indoor_property(self):
        """
        Test indoor property
        """
        test_value = True
        self.instance.indoor = test_value
        self.assertEqual(self.instance.indoor, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = SensorInfo.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = SensorInfo.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

