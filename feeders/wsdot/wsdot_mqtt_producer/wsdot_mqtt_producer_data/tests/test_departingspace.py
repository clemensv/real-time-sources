"""
Test case for DepartingSpace
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from wsdot_mqtt_producer_data.us.wa.wsdot.ferryterminals.departingspace import DepartingSpace
from wsdot_mqtt_producer_data.us.wa.wsdot.ferryterminals.spaceforarrivalterminal import SpaceForArrivalTerminal


class Test_DepartingSpace(unittest.TestCase):
    """
    Test case for DepartingSpace
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_DepartingSpace.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of DepartingSpace for testing
        """
        instance = DepartingSpace(
            departure='auwgdtyyfeuflzdegmkd',
            is_cancelled=False,
            vessel_id=int(83),
            vessel_name='gguuuuztvucwcrjzrmqt',
            max_space_count=int(16),
            space_for_arrival_terminals=[None]
        )
        return instance

    
    def test_departure_property(self):
        """
        Test departure property
        """
        test_value = 'auwgdtyyfeuflzdegmkd'
        self.instance.departure = test_value
        self.assertEqual(self.instance.departure, test_value)
    
    def test_is_cancelled_property(self):
        """
        Test is_cancelled property
        """
        test_value = False
        self.instance.is_cancelled = test_value
        self.assertEqual(self.instance.is_cancelled, test_value)
    
    def test_vessel_id_property(self):
        """
        Test vessel_id property
        """
        test_value = int(83)
        self.instance.vessel_id = test_value
        self.assertEqual(self.instance.vessel_id, test_value)
    
    def test_vessel_name_property(self):
        """
        Test vessel_name property
        """
        test_value = 'gguuuuztvucwcrjzrmqt'
        self.instance.vessel_name = test_value
        self.assertEqual(self.instance.vessel_name, test_value)
    
    def test_max_space_count_property(self):
        """
        Test max_space_count property
        """
        test_value = int(16)
        self.instance.max_space_count = test_value
        self.assertEqual(self.instance.max_space_count, test_value)
    
    def test_space_for_arrival_terminals_property(self):
        """
        Test space_for_arrival_terminals property
        """
        test_value = [None]
        self.instance.space_for_arrival_terminals = test_value
        self.assertEqual(self.instance.space_for_arrival_terminals, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = DepartingSpace.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = DepartingSpace.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

