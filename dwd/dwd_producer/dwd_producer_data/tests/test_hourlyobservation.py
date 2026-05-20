"""
Test case for HourlyObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from dwd_producer_data.hourlyobservation import HourlyObservation


class Test_HourlyObservation(unittest.TestCase):
    """
    Test case for HourlyObservation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_HourlyObservation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of HourlyObservation for testing
        """
        instance = HourlyObservation(
            station_id='whbezysxazvpruzbygpp',
            timestamp='yijydeddhswvxhpfrybg',
            quality_level=int(1),
            parameter='oceecawgbysuvtwlnufs',
            value=float(99.18777440635115),
            unit='tglizdeonvylhiyyxtvc'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'whbezysxazvpruzbygpp'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'yijydeddhswvxhpfrybg'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_quality_level_property(self):
        """
        Test quality_level property
        """
        test_value = int(1)
        self.instance.quality_level = test_value
        self.assertEqual(self.instance.quality_level, test_value)
    
    def test_parameter_property(self):
        """
        Test parameter property
        """
        test_value = 'oceecawgbysuvtwlnufs'
        self.instance.parameter = test_value
        self.assertEqual(self.instance.parameter, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(99.18777440635115)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_unit_property(self):
        """
        Test unit property
        """
        test_value = 'tglizdeonvylhiyyxtvc'
        self.instance.unit = test_value
        self.assertEqual(self.instance.unit, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = HourlyObservation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = HourlyObservation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

