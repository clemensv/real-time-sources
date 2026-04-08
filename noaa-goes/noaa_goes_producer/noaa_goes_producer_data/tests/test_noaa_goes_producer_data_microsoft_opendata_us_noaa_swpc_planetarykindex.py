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
            observation_time='hwiowxpmnarhyxlophul',
            kp=float(94.36688757596143),
            a_running=float(86.19976075727539),
            station_count=int(51)
        )
        return instance

    
    def test_observation_time_property(self):
        """
        Test observation_time property
        """
        test_value = 'hwiowxpmnarhyxlophul'
        self.instance.observation_time = test_value
        self.assertEqual(self.instance.observation_time, test_value)
    
    def test_kp_property(self):
        """
        Test kp property
        """
        test_value = float(94.36688757596143)
        self.instance.kp = test_value
        self.assertEqual(self.instance.kp, test_value)
    
    def test_a_running_property(self):
        """
        Test a_running property
        """
        test_value = float(86.19976075727539)
        self.instance.a_running = test_value
        self.assertEqual(self.instance.a_running, test_value)
    
    def test_station_count_property(self):
        """
        Test station_count property
        """
        test_value = int(51)
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
