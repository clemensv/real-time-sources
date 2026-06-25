"""
Test case for WaterLevelReading
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from ireland_opw_waterlevel_producer_data.ie.gov.opw.waterlevel.waterlevelreading import WaterLevelReading


class Test_WaterLevelReading(unittest.TestCase):
    """
    Test case for WaterLevelReading
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_WaterLevelReading.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of WaterLevelReading for testing
        """
        instance = WaterLevelReading(
            station_ref='uqohsfozjtwfbwfawpqz',
            station_name='qftstdzdqysfpmudwrxi',
            sensor_ref='xphqvwvxevuervngkgit',
            value=float(44.91717668845735),
            datetime='wdgjvdgsgrxfrjpdoowv',
            err_code=int(100),
            basin='dndiyseezupkpkuizwaz'
        )
        return instance

    
    def test_station_ref_property(self):
        """
        Test station_ref property
        """
        test_value = 'uqohsfozjtwfbwfawpqz'
        self.instance.station_ref = test_value
        self.assertEqual(self.instance.station_ref, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'qftstdzdqysfpmudwrxi'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_sensor_ref_property(self):
        """
        Test sensor_ref property
        """
        test_value = 'xphqvwvxevuervngkgit'
        self.instance.sensor_ref = test_value
        self.assertEqual(self.instance.sensor_ref, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(44.91717668845735)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'wdgjvdgsgrxfrjpdoowv'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_err_code_property(self):
        """
        Test err_code property
        """
        test_value = int(100)
        self.instance.err_code = test_value
        self.assertEqual(self.instance.err_code, test_value)
    
    def test_basin_property(self):
        """
        Test basin property
        """
        test_value = 'dndiyseezupkpkuizwaz'
        self.instance.basin = test_value
        self.assertEqual(self.instance.basin, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = WaterLevelReading.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = WaterLevelReading.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

