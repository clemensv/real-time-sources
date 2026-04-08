"""
Test case for AQHIReading
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from hongkong_epd_producer_data.aqhireading import AQHIReading
import datetime


class Test_AQHIReading(unittest.TestCase):
    """
    Test case for AQHIReading
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_AQHIReading.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of AQHIReading for testing
        """
        instance = AQHIReading(
            station_id='nooctpphvvonjqhuuufa',
            station_name='nemmudkjkifictwhlgrw',
            station_type='jkilyzbnzsbfcgcaqsws',
            reading_time=datetime.datetime.now(datetime.timezone.utc),
            aqhi=int(28),
            health_risk_category='wqffgzsgbofldcdpsgnj'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'nooctpphvvonjqhuuufa'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'nemmudkjkifictwhlgrw'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_station_type_property(self):
        """
        Test station_type property
        """
        test_value = 'jkilyzbnzsbfcgcaqsws'
        self.instance.station_type = test_value
        self.assertEqual(self.instance.station_type, test_value)
    
    def test_reading_time_property(self):
        """
        Test reading_time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.reading_time = test_value
        self.assertEqual(self.instance.reading_time, test_value)
    
    def test_aqhi_property(self):
        """
        Test aqhi property
        """
        test_value = int(28)
        self.instance.aqhi = test_value
        self.assertEqual(self.instance.aqhi, test_value)
    
    def test_health_risk_category_property(self):
        """
        Test health_risk_category property
        """
        test_value = 'wqffgzsgbofldcdpsgnj'
        self.instance.health_risk_category = test_value
        self.assertEqual(self.instance.health_risk_category, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = AQHIReading.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = AQHIReading.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

