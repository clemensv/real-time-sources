"""
Test case for Port
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from cbp_border_wait_producer_data.gov.cbp.borderwait.port import Port


class Test_Port(unittest.TestCase):
    """
    Test case for Port
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Port.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Port for testing
        """
        instance = Port(
            port_number='sbvqinevjtumzpikplfo',
            port_name='lovywrhomcdhpzycjwqz',
            border='fzefimbwvvjzgpbyjduc',
            crossing_name='mmypbnukrorzsmpqosdw',
            hours='jssmymcccauiflhmgfur',
            passenger_vehicle_max_lanes=int(16),
            commercial_vehicle_max_lanes=int(75),
            pedestrian_max_lanes=int(50)
        )
        return instance

    
    def test_port_number_property(self):
        """
        Test port_number property
        """
        test_value = 'sbvqinevjtumzpikplfo'
        self.instance.port_number = test_value
        self.assertEqual(self.instance.port_number, test_value)
    
    def test_port_name_property(self):
        """
        Test port_name property
        """
        test_value = 'lovywrhomcdhpzycjwqz'
        self.instance.port_name = test_value
        self.assertEqual(self.instance.port_name, test_value)
    
    def test_border_property(self):
        """
        Test border property
        """
        test_value = 'fzefimbwvvjzgpbyjduc'
        self.instance.border = test_value
        self.assertEqual(self.instance.border, test_value)
    
    def test_crossing_name_property(self):
        """
        Test crossing_name property
        """
        test_value = 'mmypbnukrorzsmpqosdw'
        self.instance.crossing_name = test_value
        self.assertEqual(self.instance.crossing_name, test_value)
    
    def test_hours_property(self):
        """
        Test hours property
        """
        test_value = 'jssmymcccauiflhmgfur'
        self.instance.hours = test_value
        self.assertEqual(self.instance.hours, test_value)
    
    def test_passenger_vehicle_max_lanes_property(self):
        """
        Test passenger_vehicle_max_lanes property
        """
        test_value = int(16)
        self.instance.passenger_vehicle_max_lanes = test_value
        self.assertEqual(self.instance.passenger_vehicle_max_lanes, test_value)
    
    def test_commercial_vehicle_max_lanes_property(self):
        """
        Test commercial_vehicle_max_lanes property
        """
        test_value = int(75)
        self.instance.commercial_vehicle_max_lanes = test_value
        self.assertEqual(self.instance.commercial_vehicle_max_lanes, test_value)
    
    def test_pedestrian_max_lanes_property(self):
        """
        Test pedestrian_max_lanes property
        """
        test_value = int(50)
        self.instance.pedestrian_max_lanes = test_value
        self.assertEqual(self.instance.pedestrian_max_lanes, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Port.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
