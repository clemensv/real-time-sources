"""
Test case for Measure
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from uba_airdata_amqp_producer_data.de.uba.airdata.measure import Measure


class Test_Measure(unittest.TestCase):
    """
    Test case for Measure
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Measure.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Measure for testing
        """
        instance = Measure(
            station_id=int(66),
            component_id=int(92),
            scope_id=int(93),
            date_start='mqacizmyecrgtifdvbih',
            date_end='cioejlztkioypburmqqx',
            value=float(75.61504652964292),
            quality_index='hmpqngsxiqerehceqktg'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = int(66)
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_component_id_property(self):
        """
        Test component_id property
        """
        test_value = int(92)
        self.instance.component_id = test_value
        self.assertEqual(self.instance.component_id, test_value)
    
    def test_scope_id_property(self):
        """
        Test scope_id property
        """
        test_value = int(93)
        self.instance.scope_id = test_value
        self.assertEqual(self.instance.scope_id, test_value)
    
    def test_date_start_property(self):
        """
        Test date_start property
        """
        test_value = 'mqacizmyecrgtifdvbih'
        self.instance.date_start = test_value
        self.assertEqual(self.instance.date_start, test_value)
    
    def test_date_end_property(self):
        """
        Test date_end property
        """
        test_value = 'cioejlztkioypburmqqx'
        self.instance.date_end = test_value
        self.assertEqual(self.instance.date_end, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(75.61504652964292)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_quality_index_property(self):
        """
        Test quality_index property
        """
        test_value = 'hmpqngsxiqerehceqktg'
        self.instance.quality_index = test_value
        self.assertEqual(self.instance.quality_index, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Measure.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Measure.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

