"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_bosai_amedas_mqtt_producer_data.jp.jma.amedas.station import Station
from jma_bosai_amedas_mqtt_producer_data.jp.jma.amedas.eventenum import EventEnum
from jma_bosai_amedas_mqtt_producer_data.jp.jma.amedas.stationtypeenum import StationTypeenum


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
            station_code='nshvtlojiafkjwqwyytn',
            kj_name='pphhazeexncasjhnqoek',
            kana='qozfpagqaacfokeqphxp',
            en_name='ypmvxavpzivuuuwtfvag',
            latitude=float(92.6397435674103),
            longitude=float(10.743112216419949),
            altitude_m=float(82.30292661182615),
            station_type=StationTypeenum.A,
            elems_bitmask='xscvbhryusidugtkqfwz',
            enabled_measurements=['qsinepausruejatysgrp'],
            prefecture='prtvukhtgouzlkepjngg',
            event=EventEnum.observation
        )
        return instance

    
    def test_station_code_property(self):
        """
        Test station_code property
        """
        test_value = 'nshvtlojiafkjwqwyytn'
        self.instance.station_code = test_value
        self.assertEqual(self.instance.station_code, test_value)
    
    def test_kj_name_property(self):
        """
        Test kj_name property
        """
        test_value = 'pphhazeexncasjhnqoek'
        self.instance.kj_name = test_value
        self.assertEqual(self.instance.kj_name, test_value)
    
    def test_kana_property(self):
        """
        Test kana property
        """
        test_value = 'qozfpagqaacfokeqphxp'
        self.instance.kana = test_value
        self.assertEqual(self.instance.kana, test_value)
    
    def test_en_name_property(self):
        """
        Test en_name property
        """
        test_value = 'ypmvxavpzivuuuwtfvag'
        self.instance.en_name = test_value
        self.assertEqual(self.instance.en_name, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(92.6397435674103)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(10.743112216419949)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_altitude_m_property(self):
        """
        Test altitude_m property
        """
        test_value = float(82.30292661182615)
        self.instance.altitude_m = test_value
        self.assertEqual(self.instance.altitude_m, test_value)
    
    def test_station_type_property(self):
        """
        Test station_type property
        """
        test_value = StationTypeenum.A
        self.instance.station_type = test_value
        self.assertEqual(self.instance.station_type, test_value)
    
    def test_elems_bitmask_property(self):
        """
        Test elems_bitmask property
        """
        test_value = 'xscvbhryusidugtkqfwz'
        self.instance.elems_bitmask = test_value
        self.assertEqual(self.instance.elems_bitmask, test_value)
    
    def test_enabled_measurements_property(self):
        """
        Test enabled_measurements property
        """
        test_value = ['qsinepausruejatysgrp']
        self.instance.enabled_measurements = test_value
        self.assertEqual(self.instance.enabled_measurements, test_value)
    
    def test_prefecture_property(self):
        """
        Test prefecture property
        """
        test_value = 'prtvukhtgouzlkepjngg'
        self.instance.prefecture = test_value
        self.assertEqual(self.instance.prefecture, test_value)
    
    def test_event_property(self):
        """
        Test event property
        """
        test_value = EventEnum.observation
        self.instance.event = test_value
        self.assertEqual(self.instance.event, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Station.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Station.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

