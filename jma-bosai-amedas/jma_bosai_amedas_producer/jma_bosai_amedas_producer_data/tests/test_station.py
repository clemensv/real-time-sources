"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_bosai_amedas_producer_data.jp.jma.amedas.station import Station


class Test_Station(unittest.TestCase):
    """
    Test case for Station
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Station.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Station for testing
        """
        instance = Station(
            station_code='mszbinzgrvuvnwgemmug',
            kj_name='pmpkajxfjmgsnftfucsv',
            kana='rfomodccoheinrjjgwiz',
            en_name='dkqjvlfcnrqsynlemyav',
            latitude=float(86.73060991484358),
            longitude=float(94.7797912584134),
            altitude_m=float(31.671129422356202),
            station_type='vpuueveuhnqbrltzoqks',
            elems_bitmask='pifpszdtwqqeilgglqso',
            enabled_measurements=['tfwjscilgclxpyjipnds', 'wggqgrmttammysixdfup', 'rwyynviatidtvsaszqbl']
        )
        return instance

    
    def test_station_code_property(self):
        """
        Test station_code property
        """
        test_value = 'mszbinzgrvuvnwgemmug'
        self.instance.station_code = test_value
        self.assertEqual(self.instance.station_code, test_value)
    
    def test_kj_name_property(self):
        """
        Test kj_name property
        """
        test_value = 'pmpkajxfjmgsnftfucsv'
        self.instance.kj_name = test_value
        self.assertEqual(self.instance.kj_name, test_value)
    
    def test_kana_property(self):
        """
        Test kana property
        """
        test_value = 'rfomodccoheinrjjgwiz'
        self.instance.kana = test_value
        self.assertEqual(self.instance.kana, test_value)
    
    def test_en_name_property(self):
        """
        Test en_name property
        """
        test_value = 'dkqjvlfcnrqsynlemyav'
        self.instance.en_name = test_value
        self.assertEqual(self.instance.en_name, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(86.73060991484358)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(94.7797912584134)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_altitude_m_property(self):
        """
        Test altitude_m property
        """
        test_value = float(31.671129422356202)
        self.instance.altitude_m = test_value
        self.assertEqual(self.instance.altitude_m, test_value)
    
    def test_station_type_property(self):
        """
        Test station_type property
        """
        test_value = 'vpuueveuhnqbrltzoqks'
        self.instance.station_type = test_value
        self.assertEqual(self.instance.station_type, test_value)
    
    def test_elems_bitmask_property(self):
        """
        Test elems_bitmask property
        """
        test_value = 'pifpszdtwqqeilgglqso'
        self.instance.elems_bitmask = test_value
        self.assertEqual(self.instance.elems_bitmask, test_value)
    
    def test_enabled_measurements_property(self):
        """
        Test enabled_measurements property
        """
        test_value = ['tfwjscilgclxpyjipnds', 'wggqgrmttammysixdfup', 'rwyynviatidtvsaszqbl']
        self.instance.enabled_measurements = test_value
        self.assertEqual(self.instance.enabled_measurements, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Station.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
