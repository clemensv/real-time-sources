"""
Test case for StaticDataClassB
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from kystverket_ais_producer_data.staticdataclassb import StaticDataClassB


class Test_StaticDataClassB(unittest.TestCase):
    """
    Test case for StaticDataClassB
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_StaticDataClassB.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of StaticDataClassB for testing
        """
        instance = StaticDataClassB(
            mmsi=int(64),
            part_number=int(32),
            ship_name='quepjbamhifqrvrcdpmf',
            ship_type=int(47),
            callsign='qtozzsxecmvkovpfboch',
            dimension_to_bow=int(81),
            dimension_to_stern=int(97),
            dimension_to_port=int(88),
            dimension_to_starboard=int(65),
            timestamp='gztirciinnxtownenmyv',
            station_id='nemacojlphxjmvjrvutz'
        )
        return instance

    
    def test_mmsi_property(self):
        """
        Test mmsi property
        """
        test_value = int(64)
        self.instance.mmsi = test_value
        self.assertEqual(self.instance.mmsi, test_value)
    
    def test_part_number_property(self):
        """
        Test part_number property
        """
        test_value = int(32)
        self.instance.part_number = test_value
        self.assertEqual(self.instance.part_number, test_value)
    
    def test_ship_name_property(self):
        """
        Test ship_name property
        """
        test_value = 'quepjbamhifqrvrcdpmf'
        self.instance.ship_name = test_value
        self.assertEqual(self.instance.ship_name, test_value)
    
    def test_ship_type_property(self):
        """
        Test ship_type property
        """
        test_value = int(47)
        self.instance.ship_type = test_value
        self.assertEqual(self.instance.ship_type, test_value)
    
    def test_callsign_property(self):
        """
        Test callsign property
        """
        test_value = 'qtozzsxecmvkovpfboch'
        self.instance.callsign = test_value
        self.assertEqual(self.instance.callsign, test_value)
    
    def test_dimension_to_bow_property(self):
        """
        Test dimension_to_bow property
        """
        test_value = int(81)
        self.instance.dimension_to_bow = test_value
        self.assertEqual(self.instance.dimension_to_bow, test_value)
    
    def test_dimension_to_stern_property(self):
        """
        Test dimension_to_stern property
        """
        test_value = int(97)
        self.instance.dimension_to_stern = test_value
        self.assertEqual(self.instance.dimension_to_stern, test_value)
    
    def test_dimension_to_port_property(self):
        """
        Test dimension_to_port property
        """
        test_value = int(88)
        self.instance.dimension_to_port = test_value
        self.assertEqual(self.instance.dimension_to_port, test_value)
    
    def test_dimension_to_starboard_property(self):
        """
        Test dimension_to_starboard property
        """
        test_value = int(65)
        self.instance.dimension_to_starboard = test_value
        self.assertEqual(self.instance.dimension_to_starboard, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'gztirciinnxtownenmyv'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'nemacojlphxjmvjrvutz'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = StaticDataClassB.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = StaticDataClassB.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

