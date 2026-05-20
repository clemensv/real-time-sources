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
            station_code='bnqtdzolehfcpdgcdelw',
            kj_name='mcgjczggjyvghwvuxsaz',
            kana='xgfxfwwjjqodbsxiezom',
            en_name='ltwutsjaemvaqsflffaw',
            latitude=float(75.59788951844027),
            longitude=float(27.619626336862346),
            altitude_m=float(74.81991074660424),
            station_type='tssuwmlqhdqjgzpqjesa',
            elems_bitmask='lwfevpdqtilsjorazmzb',
            enabled_measurements=['qarttyecawfrsvoveoxd', 'fdcwvbtijrnbrjqffusz']
        )
        return instance

    
    def test_station_code_property(self):
        """
        Test station_code property
        """
        test_value = 'bnqtdzolehfcpdgcdelw'
        self.instance.station_code = test_value
        self.assertEqual(self.instance.station_code, test_value)
    
    def test_kj_name_property(self):
        """
        Test kj_name property
        """
        test_value = 'mcgjczggjyvghwvuxsaz'
        self.instance.kj_name = test_value
        self.assertEqual(self.instance.kj_name, test_value)
    
    def test_kana_property(self):
        """
        Test kana property
        """
        test_value = 'xgfxfwwjjqodbsxiezom'
        self.instance.kana = test_value
        self.assertEqual(self.instance.kana, test_value)
    
    def test_en_name_property(self):
        """
        Test en_name property
        """
        test_value = 'ltwutsjaemvaqsflffaw'
        self.instance.en_name = test_value
        self.assertEqual(self.instance.en_name, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(75.59788951844027)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(27.619626336862346)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_altitude_m_property(self):
        """
        Test altitude_m property
        """
        test_value = float(74.81991074660424)
        self.instance.altitude_m = test_value
        self.assertEqual(self.instance.altitude_m, test_value)
    
    def test_station_type_property(self):
        """
        Test station_type property
        """
        test_value = 'tssuwmlqhdqjgzpqjesa'
        self.instance.station_type = test_value
        self.assertEqual(self.instance.station_type, test_value)
    
    def test_elems_bitmask_property(self):
        """
        Test elems_bitmask property
        """
        test_value = 'lwfevpdqtilsjorazmzb'
        self.instance.elems_bitmask = test_value
        self.assertEqual(self.instance.elems_bitmask, test_value)
    
    def test_enabled_measurements_property(self):
        """
        Test enabled_measurements property
        """
        test_value = ['qarttyecawfrsvoveoxd', 'fdcwvbtijrnbrjqffusz']
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
