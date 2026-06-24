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
            site_id='ycbfftopyzjttspdlkpp',
            measurement_time='gcfgnokhnatutmzujnqi',
            vehicle_flow_rate=int(60),
            average_speed=float(25.78909759965193),
            input_values_flow=int(96),
            input_values_speed=int(33)
        )
        return instance

    
    def test_site_id_property(self):
        """
        Test site_id property
        """
        test_value = 'ycbfftopyzjttspdlkpp'
        self.instance.site_id = test_value
        self.assertEqual(self.instance.site_id, test_value)
    
    def test_measurement_time_property(self):
        """
        Test measurement_time property
        """
        test_value = 'gcfgnokhnatutmzujnqi'
        self.instance.measurement_time = test_value
        self.assertEqual(self.instance.measurement_time, test_value)
    
    def test_vehicle_flow_rate_property(self):
        """
        Test vehicle_flow_rate property
        """
        test_value = int(60)
        self.instance.vehicle_flow_rate = test_value
        self.assertEqual(self.instance.vehicle_flow_rate, test_value)
    
    def test_average_speed_property(self):
        """
        Test average_speed property
        """
        test_value = float(25.78909759965193)
        self.instance.average_speed = test_value
        self.assertEqual(self.instance.average_speed, test_value)
    
    def test_input_values_flow_property(self):
        """
        Test input_values_flow property
        """
        test_value = int(96)
        self.instance.input_values_flow = test_value
        self.assertEqual(self.instance.input_values_flow, test_value)
    
    def test_input_values_speed_property(self):
        """
        Test input_values_speed property
        """
        test_value = int(33)
        self.instance.input_values_speed = test_value
        self.assertEqual(self.instance.input_values_speed, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = TrafficFlowMeasurement.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = TrafficFlowMeasurement.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

