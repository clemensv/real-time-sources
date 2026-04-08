"""
Test case for AirQualityIndex
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gios_poland_producer_data.airqualityindex import AirQualityIndex
import datetime


class Test_AirQualityIndex(unittest.TestCase):
    """
    Test case for AirQualityIndex
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_AirQualityIndex.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of AirQualityIndex for testing
        """
        instance = AirQualityIndex(
            station_id=int(3),
            calculation_timestamp=datetime.datetime.now(datetime.timezone.utc),
            index_value=int(48),
            index_category='weutxygkyhfrwttbjvfw',
            source_data_timestamp=datetime.datetime.now(datetime.timezone.utc),
            so2_calculation_timestamp=datetime.datetime.now(datetime.timezone.utc),
            so2_index_value=int(45),
            so2_index_category='zefcyppeqyrhrkxltjjw',
            so2_source_data_timestamp=datetime.datetime.now(datetime.timezone.utc),
            no2_calculation_timestamp=datetime.datetime.now(datetime.timezone.utc),
            no2_index_value=int(63),
            no2_index_category='skhaexghkqwqfpsdiufd',
            no2_source_data_timestamp=datetime.datetime.now(datetime.timezone.utc),
            pm10_calculation_timestamp=datetime.datetime.now(datetime.timezone.utc),
            pm10_index_value=int(24),
            pm10_index_category='husnwuvhtabqkynscwkz',
            pm10_source_data_timestamp=datetime.datetime.now(datetime.timezone.utc),
            pm25_calculation_timestamp=datetime.datetime.now(datetime.timezone.utc),
            pm25_index_value=int(56),
            pm25_index_category='xpewhlojcgkihtctkjjp',
            pm25_source_data_timestamp=datetime.datetime.now(datetime.timezone.utc),
            o3_calculation_timestamp=datetime.datetime.now(datetime.timezone.utc),
            o3_index_value=int(36),
            o3_index_category='tkfpujxheczxbduzqqvp',
            o3_source_data_timestamp=datetime.datetime.now(datetime.timezone.utc),
            overall_status=False,
            critical_pollutant_code='gisspskutktcndxxnqkb'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = int(3)
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_calculation_timestamp_property(self):
        """
        Test calculation_timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.calculation_timestamp = test_value
        self.assertEqual(self.instance.calculation_timestamp, test_value)
    
    def test_index_value_property(self):
        """
        Test index_value property
        """
        test_value = int(48)
        self.instance.index_value = test_value
        self.assertEqual(self.instance.index_value, test_value)
    
    def test_index_category_property(self):
        """
        Test index_category property
        """
        test_value = 'weutxygkyhfrwttbjvfw'
        self.instance.index_category = test_value
        self.assertEqual(self.instance.index_category, test_value)
    
    def test_source_data_timestamp_property(self):
        """
        Test source_data_timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.source_data_timestamp = test_value
        self.assertEqual(self.instance.source_data_timestamp, test_value)
    
    def test_so2_calculation_timestamp_property(self):
        """
        Test so2_calculation_timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.so2_calculation_timestamp = test_value
        self.assertEqual(self.instance.so2_calculation_timestamp, test_value)
    
    def test_so2_index_value_property(self):
        """
        Test so2_index_value property
        """
        test_value = int(45)
        self.instance.so2_index_value = test_value
        self.assertEqual(self.instance.so2_index_value, test_value)
    
    def test_so2_index_category_property(self):
        """
        Test so2_index_category property
        """
        test_value = 'zefcyppeqyrhrkxltjjw'
        self.instance.so2_index_category = test_value
        self.assertEqual(self.instance.so2_index_category, test_value)
    
    def test_so2_source_data_timestamp_property(self):
        """
        Test so2_source_data_timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.so2_source_data_timestamp = test_value
        self.assertEqual(self.instance.so2_source_data_timestamp, test_value)
    
    def test_no2_calculation_timestamp_property(self):
        """
        Test no2_calculation_timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.no2_calculation_timestamp = test_value
        self.assertEqual(self.instance.no2_calculation_timestamp, test_value)
    
    def test_no2_index_value_property(self):
        """
        Test no2_index_value property
        """
        test_value = int(63)
        self.instance.no2_index_value = test_value
        self.assertEqual(self.instance.no2_index_value, test_value)
    
    def test_no2_index_category_property(self):
        """
        Test no2_index_category property
        """
        test_value = 'skhaexghkqwqfpsdiufd'
        self.instance.no2_index_category = test_value
        self.assertEqual(self.instance.no2_index_category, test_value)
    
    def test_no2_source_data_timestamp_property(self):
        """
        Test no2_source_data_timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.no2_source_data_timestamp = test_value
        self.assertEqual(self.instance.no2_source_data_timestamp, test_value)
    
    def test_pm10_calculation_timestamp_property(self):
        """
        Test pm10_calculation_timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.pm10_calculation_timestamp = test_value
        self.assertEqual(self.instance.pm10_calculation_timestamp, test_value)
    
    def test_pm10_index_value_property(self):
        """
        Test pm10_index_value property
        """
        test_value = int(24)
        self.instance.pm10_index_value = test_value
        self.assertEqual(self.instance.pm10_index_value, test_value)
    
    def test_pm10_index_category_property(self):
        """
        Test pm10_index_category property
        """
        test_value = 'husnwuvhtabqkynscwkz'
        self.instance.pm10_index_category = test_value
        self.assertEqual(self.instance.pm10_index_category, test_value)
    
    def test_pm10_source_data_timestamp_property(self):
        """
        Test pm10_source_data_timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.pm10_source_data_timestamp = test_value
        self.assertEqual(self.instance.pm10_source_data_timestamp, test_value)
    
    def test_pm25_calculation_timestamp_property(self):
        """
        Test pm25_calculation_timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.pm25_calculation_timestamp = test_value
        self.assertEqual(self.instance.pm25_calculation_timestamp, test_value)
    
    def test_pm25_index_value_property(self):
        """
        Test pm25_index_value property
        """
        test_value = int(56)
        self.instance.pm25_index_value = test_value
        self.assertEqual(self.instance.pm25_index_value, test_value)
    
    def test_pm25_index_category_property(self):
        """
        Test pm25_index_category property
        """
        test_value = 'xpewhlojcgkihtctkjjp'
        self.instance.pm25_index_category = test_value
        self.assertEqual(self.instance.pm25_index_category, test_value)
    
    def test_pm25_source_data_timestamp_property(self):
        """
        Test pm25_source_data_timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.pm25_source_data_timestamp = test_value
        self.assertEqual(self.instance.pm25_source_data_timestamp, test_value)
    
    def test_o3_calculation_timestamp_property(self):
        """
        Test o3_calculation_timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.o3_calculation_timestamp = test_value
        self.assertEqual(self.instance.o3_calculation_timestamp, test_value)
    
    def test_o3_index_value_property(self):
        """
        Test o3_index_value property
        """
        test_value = int(36)
        self.instance.o3_index_value = test_value
        self.assertEqual(self.instance.o3_index_value, test_value)
    
    def test_o3_index_category_property(self):
        """
        Test o3_index_category property
        """
        test_value = 'tkfpujxheczxbduzqqvp'
        self.instance.o3_index_category = test_value
        self.assertEqual(self.instance.o3_index_category, test_value)
    
    def test_o3_source_data_timestamp_property(self):
        """
        Test o3_source_data_timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.o3_source_data_timestamp = test_value
        self.assertEqual(self.instance.o3_source_data_timestamp, test_value)
    
    def test_overall_status_property(self):
        """
        Test overall_status property
        """
        test_value = False
        self.instance.overall_status = test_value
        self.assertEqual(self.instance.overall_status, test_value)
    
    def test_critical_pollutant_code_property(self):
        """
        Test critical_pollutant_code property
        """
        test_value = 'gisspskutktcndxxnqkb'
        self.instance.critical_pollutant_code = test_value
        self.assertEqual(self.instance.critical_pollutant_code, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = AirQualityIndex.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = AirQualityIndex.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

