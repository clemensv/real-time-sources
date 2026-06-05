"""
Test case for TrafficFlowMeasurement
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from french_road_traffic_mqtt_producer_data.fr.gouv.transport.bison_fute.trafficflowmeasurement import TrafficFlowMeasurement


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
            site_id='gjxqwvkiszekhldgcrmm',
            measurement_time='bwmgfqbcshwvnaynlrxh',
            vehicle_flow_rate=int(3),
            average_speed=float(33.14097894783076),
            input_values_flow=int(97),
            input_values_speed=int(93)
        )
        return instance

    
    def test_site_id_property(self):
        """
        Test site_id property
        """
        test_value = 'gjxqwvkiszekhldgcrmm'
        self.instance.site_id = test_value
        self.assertEqual(self.instance.site_id, test_value)
    
    def test_measurement_time_property(self):
        """
        Test measurement_time property
        """
        test_value = 'bwmgfqbcshwvnaynlrxh'
        self.instance.measurement_time = test_value
        self.assertEqual(self.instance.measurement_time, test_value)
    
    def test_vehicle_flow_rate_property(self):
        """
        Test vehicle_flow_rate property
        """
        test_value = int(3)
        self.instance.vehicle_flow_rate = test_value
        self.assertEqual(self.instance.vehicle_flow_rate, test_value)
    
    def test_average_speed_property(self):
        """
        Test average_speed property
        """
        test_value = float(33.14097894783076)
        self.instance.average_speed = test_value
        self.assertEqual(self.instance.average_speed, test_value)
    
    def test_input_values_flow_property(self):
        """
        Test input_values_flow property
        """
        test_value = int(97)
        self.instance.input_values_flow = test_value
        self.assertEqual(self.instance.input_values_flow, test_value)
    
    def test_input_values_speed_property(self):
        """
        Test input_values_speed property
        """
        test_value = int(93)
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

