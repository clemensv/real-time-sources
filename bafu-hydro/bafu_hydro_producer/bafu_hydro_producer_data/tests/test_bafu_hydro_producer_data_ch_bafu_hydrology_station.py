"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from bafu_hydro_producer_data.ch.bafu.hydrology.station import Station


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
            station_id='udefgfdfclejhvqxftxm',
            name='ciplyydssczkutnghiyf',
            water_body_name='uhxwttliuhxejpdfrdvc',
            water_body_type='wtdqjzjkqcblikxnmttb',
            latitude=float(16.84993884182534),
            longitude=float(64.28881490760055)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'udefgfdfclejhvqxftxm'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'ciplyydssczkutnghiyf'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_water_body_name_property(self):
        """
        Test water_body_name property
        """
        test_value = 'uhxwttliuhxejpdfrdvc'
        self.instance.water_body_name = test_value
        self.assertEqual(self.instance.water_body_name, test_value)
    
    def test_water_body_type_property(self):
        """
        Test water_body_type property
        """
        test_value = 'wtdqjzjkqcblikxnmttb'
        self.instance.water_body_type = test_value
        self.assertEqual(self.instance.water_body_type, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(16.84993884182534)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(64.28881490760055)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Station.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
