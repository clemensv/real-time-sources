"""
Test case for DischargeObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from smhi_hydro_producer_data.dischargeobservation import DischargeObservation
import datetime


class Test_DischargeObservation(unittest.TestCase):
    """
    Test case for DischargeObservation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_DischargeObservation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of DischargeObservation for testing
        """
        instance = DischargeObservation(
            station_id='upglnwigmtyfmwlocrea',
            station_name='yyfcfnywxouwzibxrghu',
            catchment_name='gcpgmbnihgbaesyirhmy',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            discharge=float(81.60574105148697),
            quality='atdyniylvkgkrmjmsktl'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'upglnwigmtyfmwlocrea'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'yyfcfnywxouwzibxrghu'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_catchment_name_property(self):
        """
        Test catchment_name property
        """
        test_value = 'gcpgmbnihgbaesyirhmy'
        self.instance.catchment_name = test_value
        self.assertEqual(self.instance.catchment_name, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_discharge_property(self):
        """
        Test discharge property
        """
        test_value = float(81.60574105148697)
        self.instance.discharge = test_value
        self.assertEqual(self.instance.discharge, test_value)
    
    def test_quality_property(self):
        """
        Test quality property
        """
        test_value = 'atdyniylvkgkrmjmsktl'
        self.instance.quality = test_value
        self.assertEqual(self.instance.quality, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = DischargeObservation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = DischargeObservation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

