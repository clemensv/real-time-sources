"""
Test case for TimeseriesValue
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from kiwis_producer_data.timeseriesvalue import TimeseriesValue
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
            kiwis_id='srhifidnynnlujnvxtua',
            base_url='mpchvvhoheylpzfxmnso',
            ts_id='sofamutmaxrfxlzwlvaz',
            station_id='jynyuijyefytmofikdpn',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            value=float(61.53176624806894),
            quality_code=int(0),
            unit_name='urthmhevtvumltaidyud',
            unit_symbol='bkwuvdussfyujmpwplxv',
            parametertype_name='tbjynzdszuepasbnbwcy',
            stationparameter_name='brlesdpjcarqpntqbedh'
        )
        return instance

    
    def test_kiwis_id_property(self):
        """
        Test kiwis_id property
        """
        test_value = 'srhifidnynnlujnvxtua'
        self.instance.kiwis_id = test_value
        self.assertEqual(self.instance.kiwis_id, test_value)
    
    def test_base_url_property(self):
        """
        Test base_url property
        """
        test_value = 'mpchvvhoheylpzfxmnso'
        self.instance.base_url = test_value
        self.assertEqual(self.instance.base_url, test_value)
    
    def test_ts_id_property(self):
        """
        Test ts_id property
        """
        test_value = 'sofamutmaxrfxlzwlvaz'
        self.instance.ts_id = test_value
        self.assertEqual(self.instance.ts_id, test_value)
    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'jynyuijyefytmofikdpn'
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
        test_value = float(61.53176624806894)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_quality_code_property(self):
        """
        Test quality_code property
        """
        test_value = int(0)
        self.instance.quality_code = test_value
        self.assertEqual(self.instance.quality_code, test_value)
    
    def test_unit_name_property(self):
        """
        Test unit_name property
        """
        test_value = 'urthmhevtvumltaidyud'
        self.instance.unit_name = test_value
        self.assertEqual(self.instance.unit_name, test_value)
    
    def test_unit_symbol_property(self):
        """
        Test unit_symbol property
        """
        test_value = 'bkwuvdussfyujmpwplxv'
        self.instance.unit_symbol = test_value
        self.assertEqual(self.instance.unit_symbol, test_value)
    
    def test_parametertype_name_property(self):
        """
        Test parametertype_name property
        """
        test_value = 'tbjynzdszuepasbnbwcy'
        self.instance.parametertype_name = test_value
        self.assertEqual(self.instance.parametertype_name, test_value)
    
    def test_stationparameter_name_property(self):
        """
        Test stationparameter_name property
        """
        test_value = 'brlesdpjcarqpntqbedh'
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

