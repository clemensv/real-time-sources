"""
Test case for Wind
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_mqtt_producer_data.microsoft.opendata.us.noaa.wind import Wind


class Test_Wind(unittest.TestCase):
    """
    Test case for Wind
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Wind.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Wind for testing
        """
        instance = Wind(
            station_id='uztzeqlcwtmugqrruzkv',
            timestamp='jxkifubgcqemmgjugytr',
            speed=float(88.63385154981198),
            direction_degrees='ssturrwqtnsnnzaflpfx',
            direction_text='wumvitqyvquvkhbsebsc',
            gusts=float(38.748049266480024),
            max_wind_speed_exceeded=True,
            rate_of_change_exceeded=False,
            region='qrapzazvrrjipzptzind'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'uztzeqlcwtmugqrruzkv'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'jxkifubgcqemmgjugytr'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_speed_property(self):
        """
        Test speed property
        """
        test_value = float(88.63385154981198)
        self.instance.speed = test_value
        self.assertEqual(self.instance.speed, test_value)
    
    def test_direction_degrees_property(self):
        """
        Test direction_degrees property
        """
        test_value = 'ssturrwqtnsnnzaflpfx'
        self.instance.direction_degrees = test_value
        self.assertEqual(self.instance.direction_degrees, test_value)
    
    def test_direction_text_property(self):
        """
        Test direction_text property
        """
        test_value = 'wumvitqyvquvkhbsebsc'
        self.instance.direction_text = test_value
        self.assertEqual(self.instance.direction_text, test_value)
    
    def test_gusts_property(self):
        """
        Test gusts property
        """
        test_value = float(38.748049266480024)
        self.instance.gusts = test_value
        self.assertEqual(self.instance.gusts, test_value)
    
    def test_max_wind_speed_exceeded_property(self):
        """
        Test max_wind_speed_exceeded property
        """
        test_value = True
        self.instance.max_wind_speed_exceeded = test_value
        self.assertEqual(self.instance.max_wind_speed_exceeded, test_value)
    
    def test_rate_of_change_exceeded_property(self):
        """
        Test rate_of_change_exceeded property
        """
        test_value = False
        self.instance.rate_of_change_exceeded = test_value
        self.assertEqual(self.instance.rate_of_change_exceeded, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'qrapzazvrrjipzptzind'
        self.instance.region = test_value
        self.assertEqual(self.instance.region, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Wind.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Wind.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

