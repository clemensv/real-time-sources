"""
Test case for SpaceForArrivalTerminal
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from wsdot_amqp_producer_data.us.wa.wsdot.ferryterminals.spaceforarrivalterminal import SpaceForArrivalTerminal


class Test_SpaceForArrivalTerminal(unittest.TestCase):
    """
    Test case for SpaceForArrivalTerminal
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_SpaceForArrivalTerminal.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of SpaceForArrivalTerminal for testing
        """
        instance = SpaceForArrivalTerminal(
            terminal_id=int(59),
            terminal_name='imlaixtdgcceurjbrnve',
            vessel_id=int(44),
            vessel_name='neyeynocqceyyouddlug',
            display_reservable_space=True,
            reservable_space_count=int(2),
            reservable_space_hex_color='bgxrwshpxmekrlghpvwz',
            display_drive_up_space=True,
            drive_up_space_count=int(86),
            drive_up_space_hex_color='wpvqcfetrowqohabryue',
            max_space_count=int(18),
            arrival_terminal_ids=[int(70), int(100)]
        )
        return instance

    
    def test_terminal_id_property(self):
        """
        Test terminal_id property
        """
        test_value = int(59)
        self.instance.terminal_id = test_value
        self.assertEqual(self.instance.terminal_id, test_value)
    
    def test_terminal_name_property(self):
        """
        Test terminal_name property
        """
        test_value = 'imlaixtdgcceurjbrnve'
        self.instance.terminal_name = test_value
        self.assertEqual(self.instance.terminal_name, test_value)
    
    def test_vessel_id_property(self):
        """
        Test vessel_id property
        """
        test_value = int(44)
        self.instance.vessel_id = test_value
        self.assertEqual(self.instance.vessel_id, test_value)
    
    def test_vessel_name_property(self):
        """
        Test vessel_name property
        """
        test_value = 'neyeynocqceyyouddlug'
        self.instance.vessel_name = test_value
        self.assertEqual(self.instance.vessel_name, test_value)
    
    def test_display_reservable_space_property(self):
        """
        Test display_reservable_space property
        """
        test_value = True
        self.instance.display_reservable_space = test_value
        self.assertEqual(self.instance.display_reservable_space, test_value)
    
    def test_reservable_space_count_property(self):
        """
        Test reservable_space_count property
        """
        test_value = int(2)
        self.instance.reservable_space_count = test_value
        self.assertEqual(self.instance.reservable_space_count, test_value)
    
    def test_reservable_space_hex_color_property(self):
        """
        Test reservable_space_hex_color property
        """
        test_value = 'bgxrwshpxmekrlghpvwz'
        self.instance.reservable_space_hex_color = test_value
        self.assertEqual(self.instance.reservable_space_hex_color, test_value)
    
    def test_display_drive_up_space_property(self):
        """
        Test display_drive_up_space property
        """
        test_value = True
        self.instance.display_drive_up_space = test_value
        self.assertEqual(self.instance.display_drive_up_space, test_value)
    
    def test_drive_up_space_count_property(self):
        """
        Test drive_up_space_count property
        """
        test_value = int(86)
        self.instance.drive_up_space_count = test_value
        self.assertEqual(self.instance.drive_up_space_count, test_value)
    
    def test_drive_up_space_hex_color_property(self):
        """
        Test drive_up_space_hex_color property
        """
        test_value = 'wpvqcfetrowqohabryue'
        self.instance.drive_up_space_hex_color = test_value
        self.assertEqual(self.instance.drive_up_space_hex_color, test_value)
    
    def test_max_space_count_property(self):
        """
        Test max_space_count property
        """
        test_value = int(18)
        self.instance.max_space_count = test_value
        self.assertEqual(self.instance.max_space_count, test_value)
    
    def test_arrival_terminal_ids_property(self):
        """
        Test arrival_terminal_ids property
        """
        test_value = [int(70), int(100)]
        self.instance.arrival_terminal_ids = test_value
        self.assertEqual(self.instance.arrival_terminal_ids, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = SpaceForArrivalTerminal.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = SpaceForArrivalTerminal.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

