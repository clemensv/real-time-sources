"""
Test case for TrafficFlowReading
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from wsdot_producer_data.us.wa.wsdot.traffic.trafficflowreading import TrafficFlowReading


class Test_TrafficFlowReading(unittest.TestCase):
    """
    Test case for TrafficFlowReading
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_TrafficFlowReading.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of TrafficFlowReading for testing
        """
        instance = TrafficFlowReading(
            flow_data_id='whmrvfwpagvkffvnpxtz',
            station_name='bcjlfbqcebiffwmsvapr',
            region='zkkvuhehznmlhwpderki',
            flow_reading='wcpatasmypsqeiihkqiu',
            reading_time='brgrecsittlbzhdiijlt'
        )
        return instance

    
    def test_flow_data_id_property(self):
        """
        Test flow_data_id property
        """
        test_value = 'whmrvfwpagvkffvnpxtz'
        self.instance.flow_data_id = test_value
        self.assertEqual(self.instance.flow_data_id, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'bcjlfbqcebiffwmsvapr'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'zkkvuhehznmlhwpderki'
        self.instance.region = test_value
        self.assertEqual(self.instance.region, test_value)
    
    def test_flow_reading_property(self):
        """
        Test flow_reading property
        """
        test_value = 'wcpatasmypsqeiihkqiu'
        self.instance.flow_reading = test_value
        self.assertEqual(self.instance.flow_reading, test_value)
    
    def test_reading_time_property(self):
        """
        Test reading_time property
        """
        test_value = 'brgrecsittlbzhdiijlt'
        self.instance.reading_time = test_value
        self.assertEqual(self.instance.reading_time, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = TrafficFlowReading.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
