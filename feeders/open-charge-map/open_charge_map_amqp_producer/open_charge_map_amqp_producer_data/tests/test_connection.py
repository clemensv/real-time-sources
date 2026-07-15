"""
Test case for Connection
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from open_charge_map_amqp_producer_data.io.openchargemap.connection import Connection


class Test_Connection(unittest.TestCase):
    """
    Test case for Connection
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Connection.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Connection for testing
        """
        instance = Connection(
            connection_id=int(70),
            connection_type_id=int(46),
            connection_type_title='dicawtcbogpefnianvut',
            connection_type_formal_name='wqcbsccfojantisbgocf',
            reference='pajfcqboggskqwacjmhs',
            status_type_id=int(76),
            is_operational=False,
            level_id=int(83),
            level_title='jbebmcbarnqtlmwjpixb',
            is_fast_charge_capable=False,
            amps=int(3),
            voltage=int(52),
            power_kw=float(78.82780241577352),
            current_type_id=int(82),
            current_type_title='unvrqcfenrqdrxwexqqz',
            quantity=int(15),
            comments='kxpqyqcxrsqcicporxns'
        )
        return instance

    
    def test_connection_id_property(self):
        """
        Test connection_id property
        """
        test_value = int(70)
        self.instance.connection_id = test_value
        self.assertEqual(self.instance.connection_id, test_value)
    
    def test_connection_type_id_property(self):
        """
        Test connection_type_id property
        """
        test_value = int(46)
        self.instance.connection_type_id = test_value
        self.assertEqual(self.instance.connection_type_id, test_value)
    
    def test_connection_type_title_property(self):
        """
        Test connection_type_title property
        """
        test_value = 'dicawtcbogpefnianvut'
        self.instance.connection_type_title = test_value
        self.assertEqual(self.instance.connection_type_title, test_value)
    
    def test_connection_type_formal_name_property(self):
        """
        Test connection_type_formal_name property
        """
        test_value = 'wqcbsccfojantisbgocf'
        self.instance.connection_type_formal_name = test_value
        self.assertEqual(self.instance.connection_type_formal_name, test_value)
    
    def test_reference_property(self):
        """
        Test reference property
        """
        test_value = 'pajfcqboggskqwacjmhs'
        self.instance.reference = test_value
        self.assertEqual(self.instance.reference, test_value)
    
    def test_status_type_id_property(self):
        """
        Test status_type_id property
        """
        test_value = int(76)
        self.instance.status_type_id = test_value
        self.assertEqual(self.instance.status_type_id, test_value)
    
    def test_is_operational_property(self):
        """
        Test is_operational property
        """
        test_value = False
        self.instance.is_operational = test_value
        self.assertEqual(self.instance.is_operational, test_value)
    
    def test_level_id_property(self):
        """
        Test level_id property
        """
        test_value = int(83)
        self.instance.level_id = test_value
        self.assertEqual(self.instance.level_id, test_value)
    
    def test_level_title_property(self):
        """
        Test level_title property
        """
        test_value = 'jbebmcbarnqtlmwjpixb'
        self.instance.level_title = test_value
        self.assertEqual(self.instance.level_title, test_value)
    
    def test_is_fast_charge_capable_property(self):
        """
        Test is_fast_charge_capable property
        """
        test_value = False
        self.instance.is_fast_charge_capable = test_value
        self.assertEqual(self.instance.is_fast_charge_capable, test_value)
    
    def test_amps_property(self):
        """
        Test amps property
        """
        test_value = int(3)
        self.instance.amps = test_value
        self.assertEqual(self.instance.amps, test_value)
    
    def test_voltage_property(self):
        """
        Test voltage property
        """
        test_value = int(52)
        self.instance.voltage = test_value
        self.assertEqual(self.instance.voltage, test_value)
    
    def test_power_kw_property(self):
        """
        Test power_kw property
        """
        test_value = float(78.82780241577352)
        self.instance.power_kw = test_value
        self.assertEqual(self.instance.power_kw, test_value)
    
    def test_current_type_id_property(self):
        """
        Test current_type_id property
        """
        test_value = int(82)
        self.instance.current_type_id = test_value
        self.assertEqual(self.instance.current_type_id, test_value)
    
    def test_current_type_title_property(self):
        """
        Test current_type_title property
        """
        test_value = 'unvrqcfenrqdrxwexqqz'
        self.instance.current_type_title = test_value
        self.assertEqual(self.instance.current_type_title, test_value)
    
    def test_quantity_property(self):
        """
        Test quantity property
        """
        test_value = int(15)
        self.instance.quantity = test_value
        self.assertEqual(self.instance.quantity, test_value)
    
    def test_comments_property(self):
        """
        Test comments property
        """
        test_value = 'kxpqyqcxrsqcicporxns'
        self.instance.comments = test_value
        self.assertEqual(self.instance.comments, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Connection.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Connection.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

