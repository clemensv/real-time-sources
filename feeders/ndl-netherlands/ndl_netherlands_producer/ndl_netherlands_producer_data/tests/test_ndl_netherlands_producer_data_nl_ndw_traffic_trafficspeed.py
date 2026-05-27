"""
Test case for TrafficSpeed
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from ndl_netherlands_producer_data.nl.ndw.traffic.trafficspeed import TrafficSpeed


class Test_TrafficSpeed(unittest.TestCase):
    """
    Test case for TrafficSpeed
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_TrafficSpeed.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of TrafficSpeed for testing
        """
        instance = TrafficSpeed(
            site_id='xciiaclnfddqhwgreqyw',
            measurement_time='zuakxjtyoylhmnigqhdl',
            average_speed=float(14.696090649172577),
            vehicle_flow_rate=int(10),
            number_of_lanes_with_data=int(41)
        )
        return instance

    
    def test_site_id_property(self):
        """
        Test site_id property
        """
        test_value = 'xciiaclnfddqhwgreqyw'
        self.instance.site_id = test_value
        self.assertEqual(self.instance.site_id, test_value)
    
    def test_measurement_time_property(self):
        """
        Test measurement_time property
        """
        test_value = 'zuakxjtyoylhmnigqhdl'
        self.instance.measurement_time = test_value
        self.assertEqual(self.instance.measurement_time, test_value)
    
    def test_average_speed_property(self):
        """
        Test average_speed property
        """
        test_value = float(14.696090649172577)
        self.instance.average_speed = test_value
        self.assertEqual(self.instance.average_speed, test_value)
    
    def test_vehicle_flow_rate_property(self):
        """
        Test vehicle_flow_rate property
        """
        test_value = int(10)
        self.instance.vehicle_flow_rate = test_value
        self.assertEqual(self.instance.vehicle_flow_rate, test_value)
    
    def test_number_of_lanes_with_data_property(self):
        """
        Test number_of_lanes_with_data property
        """
        test_value = int(41)
        self.instance.number_of_lanes_with_data = test_value
        self.assertEqual(self.instance.number_of_lanes_with_data, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = TrafficSpeed.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
