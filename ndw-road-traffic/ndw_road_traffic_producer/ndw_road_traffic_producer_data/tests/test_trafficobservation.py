"""
Test case for TrafficObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from ndw_road_traffic_producer_data.trafficobservation import TrafficObservation


class Test_TrafficObservation(unittest.TestCase):
    """
    Test case for TrafficObservation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_TrafficObservation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of TrafficObservation for testing
        """
        instance = TrafficObservation(
            measurement_site_id='izsvuhsejbqporacbdae',
            measurement_time='erpirsuymwafajesfwwr',
            average_speed=float(82.6103800793874),
            vehicle_flow_rate=int(61),
            number_of_lanes_with_data=int(64)
        )
        return instance

    
    def test_measurement_site_id_property(self):
        """
        Test measurement_site_id property
        """
        test_value = 'izsvuhsejbqporacbdae'
        self.instance.measurement_site_id = test_value
        self.assertEqual(self.instance.measurement_site_id, test_value)
    
    def test_measurement_time_property(self):
        """
        Test measurement_time property
        """
        test_value = 'erpirsuymwafajesfwwr'
        self.instance.measurement_time = test_value
        self.assertEqual(self.instance.measurement_time, test_value)
    
    def test_average_speed_property(self):
        """
        Test average_speed property
        """
        test_value = float(82.6103800793874)
        self.instance.average_speed = test_value
        self.assertEqual(self.instance.average_speed, test_value)
    
    def test_vehicle_flow_rate_property(self):
        """
        Test vehicle_flow_rate property
        """
        test_value = int(61)
        self.instance.vehicle_flow_rate = test_value
        self.assertEqual(self.instance.vehicle_flow_rate, test_value)
    
    def test_number_of_lanes_with_data_property(self):
        """
        Test number_of_lanes_with_data property
        """
        test_value = int(64)
        self.instance.number_of_lanes_with_data = test_value
        self.assertEqual(self.instance.number_of_lanes_with_data, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = TrafficObservation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = TrafficObservation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

