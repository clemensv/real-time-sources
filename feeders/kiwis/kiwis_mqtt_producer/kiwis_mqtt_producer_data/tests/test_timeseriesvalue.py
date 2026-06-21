"""
Test case for TimeseriesValue
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from kiwis_mqtt_producer_data.timeseriesvalue import TimeseriesValue
import datetime


class Test_TimeseriesValue(unittest.TestCase):
    """
    Test case for TimeseriesValue
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_TimeseriesValue.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of TimeseriesValue for testing
        """
        instance = TimeseriesValue(
            kiwis_id='ovlkapuwwzcsqxpfcmra',
            base_url='uirbyrzzojkbrwncvmda',
            ts_id='soejozufqdkuhefxjsox',
            station_id='fwiuodbwjcmbaffzeuol',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            value=float(42.25480705651674),
            quality_code=int(44),
            unit_name='pyhfpoyucbdedropqzen',
            unit_symbol='gppebymkqwppnpiobryj',
            parametertype_name='tlaayzmsjiicftanmohc',
            stationparameter_name='jlhiwgyugcmxkzxqpaqk'
        )
        return instance

    
    def test_kiwis_id_property(self):
        """
        Test kiwis_id property
        """
        test_value = 'ovlkapuwwzcsqxpfcmra'
        self.instance.kiwis_id = test_value
        self.assertEqual(self.instance.kiwis_id, test_value)
    
    def test_base_url_property(self):
        """
        Test base_url property
        """
        test_value = 'uirbyrzzojkbrwncvmda'
        self.instance.base_url = test_value
        self.assertEqual(self.instance.base_url, test_value)
    
    def test_ts_id_property(self):
        """
        Test ts_id property
        """
        test_value = 'soejozufqdkuhefxjsox'
        self.instance.ts_id = test_value
        self.assertEqual(self.instance.ts_id, test_value)
    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'fwiuodbwjcmbaffzeuol'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(42.25480705651674)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_quality_code_property(self):
        """
        Test quality_code property
        """
        test_value = int(44)
        self.instance.quality_code = test_value
        self.assertEqual(self.instance.quality_code, test_value)
    
    def test_unit_name_property(self):
        """
        Test unit_name property
        """
        test_value = 'pyhfpoyucbdedropqzen'
        self.instance.unit_name = test_value
        self.assertEqual(self.instance.unit_name, test_value)
    
    def test_unit_symbol_property(self):
        """
        Test unit_symbol property
        """
        test_value = 'gppebymkqwppnpiobryj'
        self.instance.unit_symbol = test_value
        self.assertEqual(self.instance.unit_symbol, test_value)
    
    def test_parametertype_name_property(self):
        """
        Test parametertype_name property
        """
        test_value = 'tlaayzmsjiicftanmohc'
        self.instance.parametertype_name = test_value
        self.assertEqual(self.instance.parametertype_name, test_value)
    
    def test_stationparameter_name_property(self):
        """
        Test stationparameter_name property
        """
        test_value = 'jlhiwgyugcmxkzxqpaqk'
        self.instance.stationparameter_name = test_value
        self.assertEqual(self.instance.stationparameter_name, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = TimeseriesValue.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = TimeseriesValue.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

