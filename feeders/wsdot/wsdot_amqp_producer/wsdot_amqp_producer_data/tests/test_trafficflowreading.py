"""
Test case for TrafficFlowReading
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from wsdot_amqp_producer_data.us.wa.wsdot.traffic.trafficflowreading import TrafficFlowReading
from wsdot_amqp_producer_data.us.wa.wsdot.traffic.regionenum import RegionEnum
from wsdot_amqp_producer_data.us.wa.wsdot.traffic.flowreadingenum import FlowReadingenum


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
            flow_data_id='zcotepmbkseelgigsjyv',
            station_name='wbfmoxpuznjvatzfpnfq',
            region=RegionEnum.Eastern,
            flow_reading=FlowReadingenum.Unknown,
            reading_time='dkqjxvquufjiemrnugoa'
        )
        return instance

    
    def test_flow_data_id_property(self):
        """
        Test flow_data_id property
        """
        test_value = 'zcotepmbkseelgigsjyv'
        self.instance.flow_data_id = test_value
        self.assertEqual(self.instance.flow_data_id, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'wbfmoxpuznjvatzfpnfq'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = RegionEnum.Eastern
        self.instance.region = test_value
        self.assertEqual(self.instance.region, test_value)
    
    def test_flow_reading_property(self):
        """
        Test flow_reading property
        """
        test_value = FlowReadingenum.Unknown
        self.instance.flow_reading = test_value
        self.assertEqual(self.instance.flow_reading, test_value)
    
    def test_reading_time_property(self):
        """
        Test reading_time property
        """
        test_value = 'dkqjxvquufjiemrnugoa'
        self.instance.reading_time = test_value
        self.assertEqual(self.instance.reading_time, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = TrafficFlowReading.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = TrafficFlowReading.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

