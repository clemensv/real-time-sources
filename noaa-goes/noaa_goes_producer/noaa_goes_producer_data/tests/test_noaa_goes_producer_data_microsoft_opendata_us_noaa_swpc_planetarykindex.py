"""
Test case for PlanetaryKIndex
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_goes_producer_data.microsoft.opendata.us.noaa.swpc.planetarykindex import PlanetaryKIndex


class Test_PlanetaryKIndex(unittest.TestCase):
    """
    Test case for PlanetaryKIndex
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_PlanetaryKIndex.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of PlanetaryKIndex for testing
        """
        instance = PlanetaryKIndex(
            time_tag='ujeyxopuvpmoqpyccnat',
            kp=float(4.1264733132581615),
            a_running=float(85.68538516787305),
            station_count=float(43.108818817154)
        )
        return instance

    
    def test_time_tag_property(self):
        """
        Test time_tag property
        """
        test_value = 'ujeyxopuvpmoqpyccnat'
        self.instance.time_tag = test_value
        self.assertEqual(self.instance.time_tag, test_value)
    
    def test_kp_property(self):
        """
        Test kp property
        """
        test_value = float(4.1264733132581615)
        self.instance.kp = test_value
        self.assertEqual(self.instance.kp, test_value)
    
    def test_a_running_property(self):
        """
        Test a_running property
        """
        test_value = float(85.68538516787305)
        self.instance.a_running = test_value
        self.assertEqual(self.instance.a_running, test_value)
    
    def test_station_count_property(self):
        """
        Test station_count property
        """
        test_value = float(43.108818817154)
        self.instance.station_count = test_value
        self.assertEqual(self.instance.station_count, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = PlanetaryKIndex.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
