"""
Test case for Measure
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from uba_airdata_producer_data.de.uba.airdata.measure import Measure


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
            station_id=int(6),
            component_id=int(100),
            scope_id=int(18),
            date_start='vumhbepvpqcfnifojrwa',
            date_end='zsxrfthkyiazwnqynzqp',
            value=float(77.37281257102032),
            quality_index='rbavmexuftsalglnuzpg'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = int(6)
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_component_id_property(self):
        """
        Test component_id property
        """
        test_value = int(100)
        self.instance.component_id = test_value
        self.assertEqual(self.instance.component_id, test_value)
    
    def test_scope_id_property(self):
        """
        Test scope_id property
        """
        test_value = int(18)
        self.instance.scope_id = test_value
        self.assertEqual(self.instance.scope_id, test_value)
    
    def test_date_start_property(self):
        """
        Test date_start property
        """
        test_value = 'vumhbepvpqcfnifojrwa'
        self.instance.date_start = test_value
        self.assertEqual(self.instance.date_start, test_value)
    
    def test_date_end_property(self):
        """
        Test date_end property
        """
        test_value = 'zsxrfthkyiazwnqynzqp'
        self.instance.date_end = test_value
        self.assertEqual(self.instance.date_end, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(77.37281257102032)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_quality_index_property(self):
        """
        Test quality_index property
        """
        test_value = 'rbavmexuftsalglnuzpg'
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

