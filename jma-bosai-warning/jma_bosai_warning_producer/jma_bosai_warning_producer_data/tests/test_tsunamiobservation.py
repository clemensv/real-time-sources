"""
Test case for TsunamiObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_bosai_warning_producer_data.tsunamiobservation import TsunamiObservation
from jma_bosai_warning_producer_data.arrivalstatusenum import ArrivalStatusenum


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
            station_code='abkoeheptcxdjfxowlgq',
            station_name_jp='oextmaxwtccsxjcrvztu',
            station_name_en='vrpewblinzeqoyzeopwv',
            observed_max_wave_height_m=float(63.16023945719127),
            observed_at='ivefumgdtcexibytjuko',
            observed_at_local='blszczorajricnlnelbq',
            arrival_status=ArrivalStatusenum.ESTIMATED
        )
        return instance

    
    def test_station_code_property(self):
        """
        Test station_code property
        """
        test_value = 'abkoeheptcxdjfxowlgq'
        self.instance.station_code = test_value
        self.assertEqual(self.instance.station_code, test_value)
    
    def test_station_name_jp_property(self):
        """
        Test station_name_jp property
        """
        test_value = 'oextmaxwtccsxjcrvztu'
        self.instance.station_name_jp = test_value
        self.assertEqual(self.instance.station_name_jp, test_value)
    
    def test_station_name_en_property(self):
        """
        Test station_name_en property
        """
        test_value = 'vrpewblinzeqoyzeopwv'
        self.instance.station_name_en = test_value
        self.assertEqual(self.instance.station_name_en, test_value)
    
    def test_observed_max_wave_height_m_property(self):
        """
        Test observed_max_wave_height_m property
        """
        test_value = float(63.16023945719127)
        self.instance.observed_max_wave_height_m = test_value
        self.assertEqual(self.instance.observed_max_wave_height_m, test_value)
    
    def test_observed_at_property(self):
        """
        Test observed_at property
        """
        test_value = 'ivefumgdtcexibytjuko'
        self.instance.observed_at = test_value
        self.assertEqual(self.instance.observed_at, test_value)
    
    def test_observed_at_local_property(self):
        """
        Test observed_at_local property
        """
        test_value = 'blszczorajricnlnelbq'
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

