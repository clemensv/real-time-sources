"""
Test case for TrafficFlowMeasurement
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from french_road_traffic_producer_data.fr.gouv.transport.bison_fute.trafficflowmeasurement import TrafficFlowMeasurement


class Test_TrafficFlowMeasurement(unittest.TestCase):
    """
    Test case for TrafficFlowMeasurement
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_TrafficFlowMeasurement.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of TrafficFlowMeasurement for testing
        """
        instance = TrafficFlowMeasurement(
            site_id='fihwenkqhziawqomafba',
            measurement_time='noocsojqaesvtvizxalz',
            vehicle_flow_rate=int(84),
            average_speed=float(0.681528748458371),
            input_values_flow=int(94),
            input_values_speed=int(27)
        )
        return instance

    
    def test_site_id_property(self):
        """
        Test site_id property
        """
        test_value = 'fihwenkqhziawqomafba'
        self.instance.site_id = test_value
        self.assertEqual(self.instance.site_id, test_value)
    
    def test_measurement_time_property(self):
        """
        Test measurement_time property
        """
        test_value = 'noocsojqaesvtvizxalz'
        self.instance.measurement_time = test_value
        self.assertEqual(self.instance.measurement_time, test_value)
    
    def test_vehicle_flow_rate_property(self):
        """
        Test vehicle_flow_rate property
        """
        test_value = int(84)
        self.instance.vehicle_flow_rate = test_value
        self.assertEqual(self.instance.vehicle_flow_rate, test_value)
    
    def test_average_speed_property(self):
        """
        Test average_speed property
        """
        test_value = float(0.681528748458371)
        self.instance.average_speed = test_value
        self.assertEqual(self.instance.average_speed, test_value)
    
    def test_input_values_flow_property(self):
        """
        Test input_values_flow property
        """
        test_value = int(94)
        self.instance.input_values_flow = test_value
        self.assertEqual(self.instance.input_values_flow, test_value)
    
    def test_input_values_speed_property(self):
        """
        Test input_values_speed property
        """
        test_value = int(27)
        self.instance.input_values_speed = test_value
        self.assertEqual(self.instance.input_values_speed, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = TrafficFlowMeasurement.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
