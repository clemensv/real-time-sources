"""
Test case for TsunamiObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_bosai_warning_producer_data.tsunamiobservation import TsunamiObservation
from jma_bosai_warning_producer_data.arrivalstatusenum import ArrivalStatusenum
import datetime


class Test_TsunamiObservation(unittest.TestCase):
    """
    Test case for TsunamiObservation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_TsunamiObservation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of TsunamiObservation for testing
        """
        instance = TsunamiObservation(
            station_code='tsaclrtjjrdsswmsjole',
            station_name_jp='efbdqudacjehnsevahcq',
            station_name_en='psmzfakinbfddfqxstci',
            observed_max_wave_height_m=float(64.85674243244038),
            observed_at=datetime.datetime.now(datetime.timezone.utc),
            observed_at_local=datetime.datetime.now(datetime.timezone.utc),
            arrival_status=ArrivalStatusenum.ESTIMATED
        )
        return instance

    
    def test_station_code_property(self):
        """
        Test station_code property
        """
        test_value = 'tsaclrtjjrdsswmsjole'
        self.instance.station_code = test_value
        self.assertEqual(self.instance.station_code, test_value)
    
    def test_station_name_jp_property(self):
        """
        Test station_name_jp property
        """
        test_value = 'efbdqudacjehnsevahcq'
        self.instance.station_name_jp = test_value
        self.assertEqual(self.instance.station_name_jp, test_value)
    
    def test_station_name_en_property(self):
        """
        Test station_name_en property
        """
        test_value = 'psmzfakinbfddfqxstci'
        self.instance.station_name_en = test_value
        self.assertEqual(self.instance.station_name_en, test_value)
    
    def test_observed_max_wave_height_m_property(self):
        """
        Test observed_max_wave_height_m property
        """
        test_value = float(64.85674243244038)
        self.instance.observed_max_wave_height_m = test_value
        self.assertEqual(self.instance.observed_max_wave_height_m, test_value)
    
    def test_observed_at_property(self):
        """
        Test observed_at property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.observed_at = test_value
        self.assertEqual(self.instance.observed_at, test_value)
    
    def test_observed_at_local_property(self):
        """
        Test observed_at_local property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.observed_at_local = test_value
        self.assertEqual(self.instance.observed_at_local, test_value)
    
    def test_arrival_status_property(self):
        """
        Test arrival_status property
        """
        test_value = ArrivalStatusenum.ESTIMATED
        self.instance.arrival_status = test_value
        self.assertEqual(self.instance.arrival_status, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = TsunamiObservation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = TsunamiObservation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

