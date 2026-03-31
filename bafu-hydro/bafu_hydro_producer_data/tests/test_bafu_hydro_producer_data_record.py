"""
Test case for Record
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from bafu_hydro_producer_data.record import Record


class Test_Record(unittest.TestCase):
    """
    Test case for Record
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Record.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Record for testing
        """
        instance = Record(
            station_id='xvjosbhsesyipjnmequl',
            water_level=float(94.16655559331846),
            water_level_unit='kqlskmpzczaipzzrrvhj',
            water_level_timestamp='prshfxpgefltvabrdjmr',
            discharge=float(55.33959636776569),
            discharge_unit='dguopabyosybiqjwznbc',
            discharge_timestamp='sxztglfveucnjmvarxcl',
            water_temperature=float(29.896641171376714),
            water_temperature_unit='ksfvtbcczqlrxetamtpm',
            water_temperature_timestamp='dabfqdmwwmersvjoskjf'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'xvjosbhsesyipjnmequl'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_water_level_property(self):
        """
        Test water_level property
        """
        test_value = float(94.16655559331846)
        self.instance.water_level = test_value
        self.assertEqual(self.instance.water_level, test_value)
    
    def test_water_level_unit_property(self):
        """
        Test water_level_unit property
        """
        test_value = 'kqlskmpzczaipzzrrvhj'
        self.instance.water_level_unit = test_value
        self.assertEqual(self.instance.water_level_unit, test_value)
    
    def test_water_level_timestamp_property(self):
        """
        Test water_level_timestamp property
        """
        test_value = 'prshfxpgefltvabrdjmr'
        self.instance.water_level_timestamp = test_value
        self.assertEqual(self.instance.water_level_timestamp, test_value)
    
    def test_discharge_property(self):
        """
        Test discharge property
        """
        test_value = float(55.33959636776569)
        self.instance.discharge = test_value
        self.assertEqual(self.instance.discharge, test_value)
    
    def test_discharge_unit_property(self):
        """
        Test discharge_unit property
        """
        test_value = 'dguopabyosybiqjwznbc'
        self.instance.discharge_unit = test_value
        self.assertEqual(self.instance.discharge_unit, test_value)
    
    def test_discharge_timestamp_property(self):
        """
        Test discharge_timestamp property
        """
        test_value = 'sxztglfveucnjmvarxcl'
        self.instance.discharge_timestamp = test_value
        self.assertEqual(self.instance.discharge_timestamp, test_value)
    
    def test_water_temperature_property(self):
        """
        Test water_temperature property
        """
        test_value = float(29.896641171376714)
        self.instance.water_temperature = test_value
        self.assertEqual(self.instance.water_temperature, test_value)
    
    def test_water_temperature_unit_property(self):
        """
        Test water_temperature_unit property
        """
        test_value = 'ksfvtbcczqlrxetamtpm'
        self.instance.water_temperature_unit = test_value
        self.assertEqual(self.instance.water_temperature_unit, test_value)
    
    def test_water_temperature_timestamp_property(self):
        """
        Test water_temperature_timestamp property
        """
        test_value = 'dabfqdmwwmersvjoskjf'
        self.instance.water_temperature_timestamp = test_value
        self.assertEqual(self.instance.water_temperature_timestamp, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Record.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
