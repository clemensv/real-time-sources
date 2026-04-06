"""
Test case for ConnectorSummary
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from ndl_netherlands_producer_data.connectorsummary import ConnectorSummary
from ndl_netherlands_producer_data.formatenum import FormatEnum
from typing import Any
from ndl_netherlands_producer_data.powertypeenum import PowerTypeenum


class Test_ConnectorSummary(unittest.TestCase):
    """
    Test case for ConnectorSummary
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_ConnectorSummary.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of ConnectorSummary for testing
        """
        instance = ConnectorSummary(
            connector_id='khhplqfododddoqlybol',
            standard='nzpbjmmfsuerpvzjszbw',
            format=FormatEnum.SOCKET,
            power_type=PowerTypeenum.AC_1_PHASE,
            max_voltage=int(35),
            max_amperage=int(19),
            max_electric_power=int(6),
            tariff_ids=None
        )
        return instance

    
    def test_connector_id_property(self):
        """
        Test connector_id property
        """
        test_value = 'khhplqfododddoqlybol'
        self.instance.connector_id = test_value
        self.assertEqual(self.instance.connector_id, test_value)
    
    def test_standard_property(self):
        """
        Test standard property
        """
        test_value = 'nzpbjmmfsuerpvzjszbw'
        self.instance.standard = test_value
        self.assertEqual(self.instance.standard, test_value)
    
    def test_format_property(self):
        """
        Test format property
        """
        test_value = FormatEnum.SOCKET
        self.instance.format = test_value
        self.assertEqual(self.instance.format, test_value)
    
    def test_power_type_property(self):
        """
        Test power_type property
        """
        test_value = PowerTypeenum.AC_1_PHASE
        self.instance.power_type = test_value
        self.assertEqual(self.instance.power_type, test_value)
    
    def test_max_voltage_property(self):
        """
        Test max_voltage property
        """
        test_value = int(35)
        self.instance.max_voltage = test_value
        self.assertEqual(self.instance.max_voltage, test_value)
    
    def test_max_amperage_property(self):
        """
        Test max_amperage property
        """
        test_value = int(19)
        self.instance.max_amperage = test_value
        self.assertEqual(self.instance.max_amperage, test_value)
    
    def test_max_electric_power_property(self):
        """
        Test max_electric_power property
        """
        test_value = int(6)
        self.instance.max_electric_power = test_value
        self.assertEqual(self.instance.max_electric_power, test_value)
    
    def test_tariff_ids_property(self):
        """
        Test tariff_ids property
        """
        test_value = None
        self.instance.tariff_ids = test_value
        self.assertEqual(self.instance.tariff_ids, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = ConnectorSummary.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = ConnectorSummary.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

