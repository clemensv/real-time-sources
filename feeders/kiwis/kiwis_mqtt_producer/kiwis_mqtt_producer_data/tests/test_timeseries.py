"""
Test case for Timeseries
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from kiwis_mqtt_producer_data.timeseries import Timeseries
import datetime


class Test_Timeseries(unittest.TestCase):
    """
    Test case for Timeseries
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Timeseries.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Timeseries for testing
        """
        instance = Timeseries(
            kiwis_id='kttenwplfyfknqaqbbfr',
            base_url='vvnrcvjcgfsxhgnxjlcq',
            ts_id='thdktyqxdkmytdfadnsv',
            ts_name='gzpsikprelzndnhwcxrr',
            ts_shortname='ifintjzbbshctktcyqcj',
            station_id='ufwozhwxtyitymavhwmk',
            station_name='bpzfjyexllxrxguavnlc',
            parametertype_name='kkrmlfjloocihiiqjdiq',
            stationparameter_name='ozeriahxfjibfmkhhyvo',
            unit_name='vpyqvyqrintkakcparvm',
            unit_symbol='yjraxduxuxxtudrpreqi',
            coverage_from=datetime.datetime.now(datetime.timezone.utc),
            coverage_to=datetime.datetime.now(datetime.timezone.utc)
        )
        return instance

    
    def test_kiwis_id_property(self):
        """
        Test kiwis_id property
        """
        test_value = 'kttenwplfyfknqaqbbfr'
        self.instance.kiwis_id = test_value
        self.assertEqual(self.instance.kiwis_id, test_value)
    
    def test_base_url_property(self):
        """
        Test base_url property
        """
        test_value = 'vvnrcvjcgfsxhgnxjlcq'
        self.instance.base_url = test_value
        self.assertEqual(self.instance.base_url, test_value)
    
    def test_ts_id_property(self):
        """
        Test ts_id property
        """
        test_value = 'thdktyqxdkmytdfadnsv'
        self.instance.ts_id = test_value
        self.assertEqual(self.instance.ts_id, test_value)
    
    def test_ts_name_property(self):
        """
        Test ts_name property
        """
        test_value = 'gzpsikprelzndnhwcxrr'
        self.instance.ts_name = test_value
        self.assertEqual(self.instance.ts_name, test_value)
    
    def test_ts_shortname_property(self):
        """
        Test ts_shortname property
        """
        test_value = 'ifintjzbbshctktcyqcj'
        self.instance.ts_shortname = test_value
        self.assertEqual(self.instance.ts_shortname, test_value)
    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'ufwozhwxtyitymavhwmk'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'bpzfjyexllxrxguavnlc'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_parametertype_name_property(self):
        """
        Test parametertype_name property
        """
        test_value = 'kkrmlfjloocihiiqjdiq'
        self.instance.parametertype_name = test_value
        self.assertEqual(self.instance.parametertype_name, test_value)
    
    def test_stationparameter_name_property(self):
        """
        Test stationparameter_name property
        """
        test_value = 'ozeriahxfjibfmkhhyvo'
        self.instance.stationparameter_name = test_value
        self.assertEqual(self.instance.stationparameter_name, test_value)
    
    def test_unit_name_property(self):
        """
        Test unit_name property
        """
        test_value = 'vpyqvyqrintkakcparvm'
        self.instance.unit_name = test_value
        self.assertEqual(self.instance.unit_name, test_value)
    
    def test_unit_symbol_property(self):
        """
        Test unit_symbol property
        """
        test_value = 'yjraxduxuxxtudrpreqi'
        self.instance.unit_symbol = test_value
        self.assertEqual(self.instance.unit_symbol, test_value)
    
    def test_coverage_from_property(self):
        """
        Test coverage_from property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.coverage_from = test_value
        self.assertEqual(self.instance.coverage_from, test_value)
    
    def test_coverage_to_property(self):
        """
        Test coverage_to property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.coverage_to = test_value
        self.assertEqual(self.instance.coverage_to, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Timeseries.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Timeseries.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

