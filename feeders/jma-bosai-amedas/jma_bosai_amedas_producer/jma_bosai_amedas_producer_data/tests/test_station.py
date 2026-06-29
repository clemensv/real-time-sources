"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_bosai_amedas_producer_data.jp.jma.amedas.station import Station
from jma_bosai_amedas_producer_data.jp.jma.amedas.stationtypeenum import StationTypeenum
from jma_bosai_amedas_producer_data.jp.jma.amedas.stationeventenum import StationEventEnum


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
            station_code='fysyixaloxlivmsqcqvy',
            kj_name='wjyempddyncbkpiqgieh',
            kana='mkvnvwfcxndvjpyjupmc',
            en_name='rhltaaxdgqfuoiahtnhf',
            latitude=float(38.09493152218294),
            longitude=float(45.618616382649215),
            altitude_m=float(37.355992595096545),
            station_type=StationTypeenum.A,
            elems_bitmask='wpymjxmfwokhendocpeb',
            enabled_measurements=['zyeikdhkjqnnxtfhzrfj', 'cacgvioxyiqtcmbotakb', 'sscieyjlyrxtajtiwvlr', 'ohrumlbvqptwhvawakiq'],
            prefecture='dqmtyomjywtpyeibmntl',
            event=StationEventEnum.info
        )
        return instance

    
    def test_station_code_property(self):
        """
        Test station_code property
        """
        test_value = 'fysyixaloxlivmsqcqvy'
        self.instance.station_code = test_value
        self.assertEqual(self.instance.station_code, test_value)
    
    def test_kj_name_property(self):
        """
        Test kj_name property
        """
        test_value = 'wjyempddyncbkpiqgieh'
        self.instance.kj_name = test_value
        self.assertEqual(self.instance.kj_name, test_value)
    
    def test_kana_property(self):
        """
        Test kana property
        """
        test_value = 'mkvnvwfcxndvjpyjupmc'
        self.instance.kana = test_value
        self.assertEqual(self.instance.kana, test_value)
    
    def test_en_name_property(self):
        """
        Test en_name property
        """
        test_value = 'rhltaaxdgqfuoiahtnhf'
        self.instance.en_name = test_value
        self.assertEqual(self.instance.en_name, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(38.09493152218294)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(45.618616382649215)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_altitude_m_property(self):
        """
        Test altitude_m property
        """
        test_value = float(37.355992595096545)
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
        test_value = 'wpymjxmfwokhendocpeb'
        self.instance.elems_bitmask = test_value
        self.assertEqual(self.instance.elems_bitmask, test_value)
    
    def test_enabled_measurements_property(self):
        """
        Test enabled_measurements property
        """
        test_value = ['zyeikdhkjqnnxtfhzrfj', 'cacgvioxyiqtcmbotakb', 'sscieyjlyrxtajtiwvlr', 'ohrumlbvqptwhvawakiq']
        self.instance.enabled_measurements = test_value
        self.assertEqual(self.instance.enabled_measurements, test_value)
    
    def test_prefecture_property(self):
        """
        Test prefecture property
        """
        test_value = 'dqmtyomjywtpyeibmntl'
        self.instance.prefecture = test_value
        self.assertEqual(self.instance.prefecture, test_value)
    
    def test_event_property(self):
        """
        Test event property
        """
        test_value = StationEventEnum.info
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

