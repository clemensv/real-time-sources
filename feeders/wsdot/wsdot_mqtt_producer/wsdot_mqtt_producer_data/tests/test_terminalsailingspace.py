"""
Test case for TerminalSailingSpace
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from wsdot_mqtt_producer_data.us.wa.wsdot.ferryterminals.terminalsailingspace import TerminalSailingSpace
from wsdot_mqtt_producer_data.us.wa.wsdot.ferryterminals.departingspace import DepartingSpace


class Test_TerminalSailingSpace(unittest.TestCase):
    """
    Test case for TerminalSailingSpace
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_TerminalSailingSpace.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of TerminalSailingSpace for testing
        """
        instance = TerminalSailingSpace(
            terminal_id='nukbgmgjkefcdosxgjry',
            terminal_subject_id=int(69),
            region_id=int(55),
            terminal_name='ykyjargjckhrzbmfohhu',
            terminal_abbrev='qwjdngoznchsnfcbmora',
            sort_seq=int(7),
            departing_spaces=[None],
            is_no_fare_collected=False,
            no_fare_collected_msg='zalsgncygcsaforrnxlb'
        )
        return instance

    
    def test_terminal_id_property(self):
        """
        Test terminal_id property
        """
        test_value = 'nukbgmgjkefcdosxgjry'
        self.instance.terminal_id = test_value
        self.assertEqual(self.instance.terminal_id, test_value)
    
    def test_terminal_subject_id_property(self):
        """
        Test terminal_subject_id property
        """
        test_value = int(69)
        self.instance.terminal_subject_id = test_value
        self.assertEqual(self.instance.terminal_subject_id, test_value)
    
    def test_region_id_property(self):
        """
        Test region_id property
        """
        test_value = int(55)
        self.instance.region_id = test_value
        self.assertEqual(self.instance.region_id, test_value)
    
    def test_terminal_name_property(self):
        """
        Test terminal_name property
        """
        test_value = 'ykyjargjckhrzbmfohhu'
        self.instance.terminal_name = test_value
        self.assertEqual(self.instance.terminal_name, test_value)
    
    def test_terminal_abbrev_property(self):
        """
        Test terminal_abbrev property
        """
        test_value = 'qwjdngoznchsnfcbmora'
        self.instance.terminal_abbrev = test_value
        self.assertEqual(self.instance.terminal_abbrev, test_value)
    
    def test_sort_seq_property(self):
        """
        Test sort_seq property
        """
        test_value = int(7)
        self.instance.sort_seq = test_value
        self.assertEqual(self.instance.sort_seq, test_value)
    
    def test_departing_spaces_property(self):
        """
        Test departing_spaces property
        """
        test_value = [None]
        self.instance.departing_spaces = test_value
        self.assertEqual(self.instance.departing_spaces, test_value)
    
    def test_is_no_fare_collected_property(self):
        """
        Test is_no_fare_collected property
        """
        test_value = False
        self.instance.is_no_fare_collected = test_value
        self.assertEqual(self.instance.is_no_fare_collected, test_value)
    
    def test_no_fare_collected_msg_property(self):
        """
        Test no_fare_collected_msg property
        """
        test_value = 'zalsgncygcsaforrnxlb'
        self.instance.no_fare_collected_msg = test_value
        self.assertEqual(self.instance.no_fare_collected_msg, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = TerminalSailingSpace.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = TerminalSailingSpace.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

