"""
Test case for AidToNavigation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from kystverket_ais_producer_data.no.kystverket.ais.aidtonavigation import AidToNavigation


class Test_AidToNavigation(unittest.TestCase):
    """
    Test case for AidToNavigation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_AidToNavigation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of AidToNavigation for testing
        """
        instance = AidToNavigation(
            mmsi=int(87),
            aid_type=int(13),
            name='nyqsoitzpkibtyuljfgp',
            position_accuracy=int(35),
            longitude=float(72.35034302967486),
            latitude=float(61.64442694935699),
            timestamp='tsfxzcaxdhgkdzzxnpeb',
            station_id='whivyqtjfwflnwcxirso'
        )
        return instance

    
    def test_mmsi_property(self):
        """
        Test mmsi property
        """
        test_value = int(87)
        self.instance.mmsi = test_value
        self.assertEqual(self.instance.mmsi, test_value)
    
    def test_aid_type_property(self):
        """
        Test aid_type property
        """
        test_value = int(13)
        self.instance.aid_type = test_value
        self.assertEqual(self.instance.aid_type, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'nyqsoitzpkibtyuljfgp'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_position_accuracy_property(self):
        """
        Test position_accuracy property
        """
        test_value = int(35)
        self.instance.position_accuracy = test_value
        self.assertEqual(self.instance.position_accuracy, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(72.35034302967486)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(61.64442694935699)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'tsfxzcaxdhgkdzzxnpeb'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'whivyqtjfwflnwcxirso'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = AidToNavigation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
