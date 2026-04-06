"""
Test case for Salinity
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_producer_data.microsoft.opendata.us.noaa.salinity import Salinity


class Test_Salinity(unittest.TestCase):
    """
    Test case for Salinity
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Salinity.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Salinity for testing
        """
        instance = Salinity(
            station_id='zxutjkrjqwyobyfbbqyn',
            timestamp='pqemetwozcyvagpdjhbw',
            salinity=float(35.25668152845613),
            grams_per_kg=float(71.3640997470257)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'zxutjkrjqwyobyfbbqyn'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'pqemetwozcyvagpdjhbw'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_salinity_property(self):
        """
        Test salinity property
        """
        test_value = float(35.25668152845613)
        self.instance.salinity = test_value
        self.assertEqual(self.instance.salinity, test_value)
    
    def test_grams_per_kg_property(self):
        """
        Test grams_per_kg property
        """
        test_value = float(71.3640997470257)
        self.instance.grams_per_kg = test_value
        self.assertEqual(self.instance.grams_per_kg, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Salinity.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
