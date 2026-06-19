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
            mmsi=int(9),
            part_number=int(86),
            ship_name='vbeebrtnuqpnfosadftl',
            ship_type=int(90),
            callsign='jkytgccibdejyvrzyoqm',
            dimension_to_bow=int(54),
            dimension_to_stern=int(69),
            dimension_to_port=int(78),
            dimension_to_starboard=int(28),
            timestamp='babnqkvhowkwukpxogdc',
            station_id='nwgbbaubaqdxilyertyd'
        )
        return instance

    
    def test_mmsi_property(self):
        """
        Test mmsi property
        """
        test_value = int(9)
        self.instance.mmsi = test_value
        self.assertEqual(self.instance.mmsi, test_value)
    
    def test_part_number_property(self):
        """
        Test part_number property
        """
        test_value = int(86)
        self.instance.part_number = test_value
        self.assertEqual(self.instance.part_number, test_value)
    
    def test_ship_name_property(self):
        """
        Test ship_name property
        """
        test_value = 'vbeebrtnuqpnfosadftl'
        self.instance.ship_name = test_value
        self.assertEqual(self.instance.ship_name, test_value)
    
    def test_ship_type_property(self):
        """
        Test ship_type property
        """
        test_value = int(90)
        self.instance.ship_type = test_value
        self.assertEqual(self.instance.ship_type, test_value)
    
    def test_callsign_property(self):
        """
        Test callsign property
        """
        test_value = 'jkytgccibdejyvrzyoqm'
        self.instance.callsign = test_value
        self.assertEqual(self.instance.callsign, test_value)
    
    def test_dimension_to_bow_property(self):
        """
        Test dimension_to_bow property
        """
        test_value = int(54)
        self.instance.dimension_to_bow = test_value
        self.assertEqual(self.instance.dimension_to_bow, test_value)
    
    def test_dimension_to_stern_property(self):
        """
        Test dimension_to_stern property
        """
        test_value = int(69)
        self.instance.dimension_to_stern = test_value
        self.assertEqual(self.instance.dimension_to_stern, test_value)
    
    def test_dimension_to_port_property(self):
        """
        Test dimension_to_port property
        """
        test_value = int(78)
        self.instance.dimension_to_port = test_value
        self.assertEqual(self.instance.dimension_to_port, test_value)
    
    def test_dimension_to_starboard_property(self):
        """
        Test dimension_to_starboard property
        """
        test_value = int(28)
        self.instance.dimension_to_starboard = test_value
        self.assertEqual(self.instance.dimension_to_starboard, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'babnqkvhowkwukpxogdc'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'nwgbbaubaqdxilyertyd'
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

