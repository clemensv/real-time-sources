"""
Test case for DoseRateReading
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from eurdep_radiation_producer_data.eu.jrc.eurdep.doseratereading import DoseRateReading


class Test_DoseRateReading(unittest.TestCase):
    """
    Test case for DoseRateReading
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_DoseRateReading.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of DoseRateReading for testing
        """
        instance = DoseRateReading(
            station_id='wemvybrmqwyshykmtfal',
            name='wfyxgpbhihfhhockpczz',
            value=float(75.26643190460157),
            unit='ifafznwkszlkrhtrdmxp',
            start_measure='hiipltuvkmornvsqhjiv',
            end_measure='xmnxiovskmltxhhyaplw',
            nuclide='bgighkkpeiatpklacgam',
            duration='oujtdnlpscqngwapvpeo',
            validated=int(67)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'wemvybrmqwyshykmtfal'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'wfyxgpbhihfhhockpczz'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(75.26643190460157)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_unit_property(self):
        """
        Test unit property
        """
        test_value = 'ifafznwkszlkrhtrdmxp'
        self.instance.unit = test_value
        self.assertEqual(self.instance.unit, test_value)
    
    def test_start_measure_property(self):
        """
        Test start_measure property
        """
        test_value = 'hiipltuvkmornvsqhjiv'
        self.instance.start_measure = test_value
        self.assertEqual(self.instance.start_measure, test_value)
    
    def test_end_measure_property(self):
        """
        Test end_measure property
        """
        test_value = 'xmnxiovskmltxhhyaplw'
        self.instance.end_measure = test_value
        self.assertEqual(self.instance.end_measure, test_value)
    
    def test_nuclide_property(self):
        """
        Test nuclide property
        """
        test_value = 'bgighkkpeiatpklacgam'
        self.instance.nuclide = test_value
        self.assertEqual(self.instance.nuclide, test_value)
    
    def test_duration_property(self):
        """
        Test duration property
        """
        test_value = 'oujtdnlpscqngwapvpeo'
        self.instance.duration = test_value
        self.assertEqual(self.instance.duration, test_value)
    
    def test_validated_property(self):
        """
        Test validated property
        """
        test_value = int(67)
        self.instance.validated = test_value
        self.assertEqual(self.instance.validated, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = DoseRateReading.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
