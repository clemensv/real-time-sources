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
            connection_id=int(51),
            connection_type_id=int(3),
            connection_type_title='ukymmhikqxttevbtotek',
            connection_type_formal_name='mibgqwesonicrnzramsl',
            reference='cofrztwfihvyndpfkfzw',
            status_type_id=int(76),
            is_operational=False,
            level_id=int(55),
            level_title='lfipnqdhnsysxkhrpltu',
            is_fast_charge_capable=True,
            amps=int(26),
            voltage=int(3),
            power_kw=float(20.60514615181691),
            current_type_id=int(97),
            current_type_title='bubyiboqzaslncpccmef',
            quantity=int(47),
            comments='ifazampgyhcqokqkdaxl'
        )
        return instance

    
    def test_connection_id_property(self):
        """
        Test connection_id property
        """
        test_value = int(51)
        self.instance.connection_id = test_value
        self.assertEqual(self.instance.connection_id, test_value)
    
    def test_connection_type_id_property(self):
        """
        Test connection_type_id property
        """
        test_value = int(3)
        self.instance.connection_type_id = test_value
        self.assertEqual(self.instance.connection_type_id, test_value)
    
    def test_connection_type_title_property(self):
        """
        Test connection_type_title property
        """
        test_value = 'ukymmhikqxttevbtotek'
        self.instance.connection_type_title = test_value
        self.assertEqual(self.instance.connection_type_title, test_value)
    
    def test_connection_type_formal_name_property(self):
        """
        Test connection_type_formal_name property
        """
        test_value = 'mibgqwesonicrnzramsl'
        self.instance.connection_type_formal_name = test_value
        self.assertEqual(self.instance.connection_type_formal_name, test_value)
    
    def test_reference_property(self):
        """
        Test reference property
        """
        test_value = 'cofrztwfihvyndpfkfzw'
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
        test_value = int(55)
        self.instance.level_id = test_value
        self.assertEqual(self.instance.level_id, test_value)
    
    def test_level_title_property(self):
        """
        Test level_title property
        """
        test_value = 'lfipnqdhnsysxkhrpltu'
        self.instance.level_title = test_value
        self.assertEqual(self.instance.level_title, test_value)
    
    def test_is_fast_charge_capable_property(self):
        """
        Test is_fast_charge_capable property
        """
        test_value = True
        self.instance.is_fast_charge_capable = test_value
        self.assertEqual(self.instance.is_fast_charge_capable, test_value)
    
    def test_amps_property(self):
        """
        Test amps property
        """
        test_value = int(26)
        self.instance.amps = test_value
        self.assertEqual(self.instance.amps, test_value)
    
    def test_voltage_property(self):
        """
        Test voltage property
        """
        test_value = int(3)
        self.instance.voltage = test_value
        self.assertEqual(self.instance.voltage, test_value)
    
    def test_power_kw_property(self):
        """
        Test power_kw property
        """
        test_value = float(20.60514615181691)
        self.instance.power_kw = test_value
        self.assertEqual(self.instance.power_kw, test_value)
    
    def test_current_type_id_property(self):
        """
        Test current_type_id property
        """
        test_value = int(97)
        self.instance.current_type_id = test_value
        self.assertEqual(self.instance.current_type_id, test_value)
    
    def test_current_type_title_property(self):
        """
        Test current_type_title property
        """
        test_value = 'bubyiboqzaslncpccmef'
        self.instance.current_type_title = test_value
        self.assertEqual(self.instance.current_type_title, test_value)
    
    def test_quantity_property(self):
        """
        Test quantity property
        """
        test_value = int(47)
        self.instance.quantity = test_value
        self.assertEqual(self.instance.quantity, test_value)
    
    def test_comments_property(self):
        """
        Test comments property
        """
        test_value = 'ifazampgyhcqokqkdaxl'
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

