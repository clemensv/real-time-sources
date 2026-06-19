"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from ireland_opw_waterlevel_amqp_producer_data.ie.gov.opw.waterlevel.station import Station


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
            station_ref='gwqzmawhyvffztesxgcf',
            station_name='vbiraiqizbxerufkicso',
            region_id=int(87),
            longitude=float(34.312624508719345),
            latitude=float(91.29517210593458),
            basin='xhcrbgdmffxuoioodpmb'
        )
        return instance

    
    def test_station_ref_property(self):
        """
        Test station_ref property
        """
        test_value = 'gwqzmawhyvffztesxgcf'
        self.instance.station_ref = test_value
        self.assertEqual(self.instance.station_ref, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'vbiraiqizbxerufkicso'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_region_id_property(self):
        """
        Test region_id property
        """
        test_value = int(87)
        self.instance.region_id = test_value
        self.assertEqual(self.instance.region_id, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(34.312624508719345)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(91.29517210593458)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_basin_property(self):
        """
        Test basin property
        """
        test_value = 'xhcrbgdmffxuoioodpmb'
        self.instance.basin = test_value
        self.assertEqual(self.instance.basin, test_value)
    
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

