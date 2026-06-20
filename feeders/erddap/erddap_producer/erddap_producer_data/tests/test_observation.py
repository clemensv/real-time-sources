"""
Test case for Observation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from erddap_producer_data.observation import Observation
from erddap_producer_data.measurementvalue import MeasurementValue


class Test_Observation(unittest.TestCase):
    """
    Test case for Observation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Observation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Observation for testing
        """
        instance = Observation(
            erddap_id='gbhcunyzucznbsdmwgbm',
            dataset_id='hmzorzbdrafvbavbphuq',
            base_url='wsqsswrctufidbcigckh',
            station_id='vvvgzvsacakupdgsmlqq',
            time='uanckkdkoknkawrggxxq',
            latitude=float(79.99788349928745),
            longitude=float(76.58238864356107),
            depth=float(8.164878124330855),
            measurements={'mbyjujfselvseegohnyv': None, 'ziksgqqjjedtlpjmmkok': None, 'hthvamkilqsqenlzvexs': None, 'ciqzabtfwlbauxwrcagv': None}
        )
        return instance

    
    def test_erddap_id_property(self):
        """
        Test erddap_id property
        """
        test_value = 'gbhcunyzucznbsdmwgbm'
        self.instance.erddap_id = test_value
        self.assertEqual(self.instance.erddap_id, test_value)
    
    def test_dataset_id_property(self):
        """
        Test dataset_id property
        """
        test_value = 'hmzorzbdrafvbavbphuq'
        self.instance.dataset_id = test_value
        self.assertEqual(self.instance.dataset_id, test_value)
    
    def test_base_url_property(self):
        """
        Test base_url property
        """
        test_value = 'wsqsswrctufidbcigckh'
        self.instance.base_url = test_value
        self.assertEqual(self.instance.base_url, test_value)
    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'vvvgzvsacakupdgsmlqq'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_time_property(self):
        """
        Test time property
        """
        test_value = 'uanckkdkoknkawrggxxq'
        self.instance.time = test_value
        self.assertEqual(self.instance.time, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(79.99788349928745)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(76.58238864356107)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_depth_property(self):
        """
        Test depth property
        """
        test_value = float(8.164878124330855)
        self.instance.depth = test_value
        self.assertEqual(self.instance.depth, test_value)
    
    def test_measurements_property(self):
        """
        Test measurements property
        """
        test_value = {'mbyjujfselvseegohnyv': None, 'ziksgqqjjedtlpjmmkok': None, 'hthvamkilqsqenlzvexs': None, 'ciqzabtfwlbauxwrcagv': None}
        self.instance.measurements = test_value
        self.assertEqual(self.instance.measurements, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Observation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Observation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

