"""
Test case for AidToNavigation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from kystverket_ais_producer_data.aidtonavigation import AidToNavigation


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
            mmsi=int(14),
            aid_type=int(32),
            name='eonvgdgirofbmjbckotq',
            position_accuracy=int(61),
            longitude=float(5.857311223205541),
            latitude=float(43.104577495457285),
            timestamp='iflpestbzmjojfdwbjwl',
            station_id='rrcqoeopemadatowyoyu'
        )
        return instance

    
    def test_mmsi_property(self):
        """
        Test mmsi property
        """
        test_value = int(14)
        self.instance.mmsi = test_value
        self.assertEqual(self.instance.mmsi, test_value)
    
    def test_aid_type_property(self):
        """
        Test aid_type property
        """
        test_value = int(32)
        self.instance.aid_type = test_value
        self.assertEqual(self.instance.aid_type, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'eonvgdgirofbmjbckotq'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_position_accuracy_property(self):
        """
        Test position_accuracy property
        """
        test_value = int(61)
        self.instance.position_accuracy = test_value
        self.assertEqual(self.instance.position_accuracy, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(5.857311223205541)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(43.104577495457285)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'iflpestbzmjojfdwbjwl'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'rrcqoeopemadatowyoyu'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = AidToNavigation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = AidToNavigation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

