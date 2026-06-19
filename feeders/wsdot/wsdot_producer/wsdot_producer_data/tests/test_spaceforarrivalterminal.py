"""
Test case for SpaceForArrivalTerminal
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from wsdot_producer_data.us.wa.wsdot.ferryterminals.spaceforarrivalterminal import SpaceForArrivalTerminal


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
            terminal_id=int(4),
            terminal_name='pokcgmgyqkffzamqnjcb',
            vessel_id=int(17),
            vessel_name='uwggjfbgfgcpurgrvffx',
            display_reservable_space=True,
            reservable_space_count=int(54),
            reservable_space_hex_color='ejpxjjnatsmjpuvvsips',
            display_drive_up_space=False,
            drive_up_space_count=int(49),
            drive_up_space_hex_color='eswlwuishjknutkhmkow',
            max_space_count=int(6),
            arrival_terminal_ids=[int(83), int(87)]
        )
        return instance

    
    def test_terminal_id_property(self):
        """
        Test terminal_id property
        """
        test_value = int(4)
        self.instance.terminal_id = test_value
        self.assertEqual(self.instance.terminal_id, test_value)
    
    def test_terminal_name_property(self):
        """
        Test terminal_name property
        """
        test_value = 'pokcgmgyqkffzamqnjcb'
        self.instance.terminal_name = test_value
        self.assertEqual(self.instance.terminal_name, test_value)
    
    def test_vessel_id_property(self):
        """
        Test vessel_id property
        """
        test_value = int(17)
        self.instance.vessel_id = test_value
        self.assertEqual(self.instance.vessel_id, test_value)
    
    def test_vessel_name_property(self):
        """
        Test vessel_name property
        """
        test_value = 'uwggjfbgfgcpurgrvffx'
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
        test_value = int(54)
        self.instance.reservable_space_count = test_value
        self.assertEqual(self.instance.reservable_space_count, test_value)
    
    def test_reservable_space_hex_color_property(self):
        """
        Test reservable_space_hex_color property
        """
        test_value = 'ejpxjjnatsmjpuvvsips'
        self.instance.reservable_space_hex_color = test_value
        self.assertEqual(self.instance.reservable_space_hex_color, test_value)
    
    def test_display_drive_up_space_property(self):
        """
        Test display_drive_up_space property
        """
        test_value = False
        self.instance.display_drive_up_space = test_value
        self.assertEqual(self.instance.display_drive_up_space, test_value)
    
    def test_drive_up_space_count_property(self):
        """
        Test drive_up_space_count property
        """
        test_value = int(49)
        self.instance.drive_up_space_count = test_value
        self.assertEqual(self.instance.drive_up_space_count, test_value)
    
    def test_drive_up_space_hex_color_property(self):
        """
        Test drive_up_space_hex_color property
        """
        test_value = 'eswlwuishjknutkhmkow'
        self.instance.drive_up_space_hex_color = test_value
        self.assertEqual(self.instance.drive_up_space_hex_color, test_value)
    
    def test_max_space_count_property(self):
        """
        Test max_space_count property
        """
        test_value = int(6)
        self.instance.max_space_count = test_value
        self.assertEqual(self.instance.max_space_count, test_value)
    
    def test_arrival_terminal_ids_property(self):
        """
        Test arrival_terminal_ids property
        """
        test_value = [int(83), int(87)]
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

