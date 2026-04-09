"""
Test case for Measurement
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from airqo_uganda_producer_data.measurement import Measurement
import datetime


class Test_Measurement(unittest.TestCase):
    """
    Test case for Measurement
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Measurement.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Measurement for testing
        """
        instance = Measurement(
            site_id='rsulppisavubfumehzct',
            device='ctruzgiqccevnnqltcxr',
            device_id='vuoeihnclmgmdpxglnuy',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            pm2_5_raw=float(57.77992876404063),
            pm2_5_calibrated=float(18.963374625158124),
            pm10_raw=float(44.06339351543889),
            pm10_calibrated=float(76.08755802323815),
            temperature=float(47.96793405773966),
            humidity=float(16.899526505363916),
            latitude=float(99.66292758984599),
            longitude=float(19.301123493219883),
            frequency='cudjifhxokgvqhwcjidl'
        )
        return instance

    
    def test_site_id_property(self):
        """
        Test site_id property
        """
        test_value = 'rsulppisavubfumehzct'
        self.instance.site_id = test_value
        self.assertEqual(self.instance.site_id, test_value)
    
    def test_device_property(self):
        """
        Test device property
        """
        test_value = 'ctruzgiqccevnnqltcxr'
        self.instance.device = test_value
        self.assertEqual(self.instance.device, test_value)
    
    def test_device_id_property(self):
        """
        Test device_id property
        """
        test_value = 'vuoeihnclmgmdpxglnuy'
        self.instance.device_id = test_value
        self.assertEqual(self.instance.device_id, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_pm2_5_raw_property(self):
        """
        Test pm2_5_raw property
        """
        test_value = float(57.77992876404063)
        self.instance.pm2_5_raw = test_value
        self.assertEqual(self.instance.pm2_5_raw, test_value)
    
    def test_pm2_5_calibrated_property(self):
        """
        Test pm2_5_calibrated property
        """
        test_value = float(18.963374625158124)
        self.instance.pm2_5_calibrated = test_value
        self.assertEqual(self.instance.pm2_5_calibrated, test_value)
    
    def test_pm10_raw_property(self):
        """
        Test pm10_raw property
        """
        test_value = float(44.06339351543889)
        self.instance.pm10_raw = test_value
        self.assertEqual(self.instance.pm10_raw, test_value)
    
    def test_pm10_calibrated_property(self):
        """
        Test pm10_calibrated property
        """
        test_value = float(76.08755802323815)
        self.instance.pm10_calibrated = test_value
        self.assertEqual(self.instance.pm10_calibrated, test_value)
    
    def test_temperature_property(self):
        """
        Test temperature property
        """
        test_value = float(47.96793405773966)
        self.instance.temperature = test_value
        self.assertEqual(self.instance.temperature, test_value)
    
    def test_humidity_property(self):
        """
        Test humidity property
        """
        test_value = float(16.899526505363916)
        self.instance.humidity = test_value
        self.assertEqual(self.instance.humidity, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(99.66292758984599)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(19.301123493219883)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_frequency_property(self):
        """
        Test frequency property
        """
        test_value = 'cudjifhxokgvqhwcjidl'
        self.instance.frequency = test_value
        self.assertEqual(self.instance.frequency, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Measurement.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Measurement.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

