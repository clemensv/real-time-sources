"""
Test case for StaticVoyageData
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from kystverket_ais_producer_data.staticvoyagedata import StaticVoyageData


class Test_StaticVoyageData(unittest.TestCase):
    """
    Test case for StaticVoyageData
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_StaticVoyageData.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of StaticVoyageData for testing
        """
        instance = StaticVoyageData(
            mmsi=int(29),
            imo_number=int(87),
            callsign='mhwhukdjzmpssmavptuo',
            ship_name='pvfojemewwmymbkhgvbp',
            ship_type=int(92),
            dimension_to_bow=int(100),
            dimension_to_stern=int(1),
            dimension_to_port=int(36),
            dimension_to_starboard=int(92),
            draught=float(18.983977035719303),
            destination='htzmuemrrtysqbdqqzxs',
            eta_month=int(77),
            eta_day=int(47),
            eta_hour=int(71),
            eta_minute=int(97),
            timestamp='rohsxlbvfrnutyzhwarb',
            station_id='odeeaghohrulnxxzgmga'
        )
        return instance

    
    def test_mmsi_property(self):
        """
        Test mmsi property
        """
        test_value = int(29)
        self.instance.mmsi = test_value
        self.assertEqual(self.instance.mmsi, test_value)
    
    def test_imo_number_property(self):
        """
        Test imo_number property
        """
        test_value = int(87)
        self.instance.imo_number = test_value
        self.assertEqual(self.instance.imo_number, test_value)
    
    def test_callsign_property(self):
        """
        Test callsign property
        """
        test_value = 'mhwhukdjzmpssmavptuo'
        self.instance.callsign = test_value
        self.assertEqual(self.instance.callsign, test_value)
    
    def test_ship_name_property(self):
        """
        Test ship_name property
        """
        test_value = 'pvfojemewwmymbkhgvbp'
        self.instance.ship_name = test_value
        self.assertEqual(self.instance.ship_name, test_value)
    
    def test_ship_type_property(self):
        """
        Test ship_type property
        """
        test_value = int(92)
        self.instance.ship_type = test_value
        self.assertEqual(self.instance.ship_type, test_value)
    
    def test_dimension_to_bow_property(self):
        """
        Test dimension_to_bow property
        """
        test_value = int(100)
        self.instance.dimension_to_bow = test_value
        self.assertEqual(self.instance.dimension_to_bow, test_value)
    
    def test_dimension_to_stern_property(self):
        """
        Test dimension_to_stern property
        """
        test_value = int(1)
        self.instance.dimension_to_stern = test_value
        self.assertEqual(self.instance.dimension_to_stern, test_value)
    
    def test_dimension_to_port_property(self):
        """
        Test dimension_to_port property
        """
        test_value = int(36)
        self.instance.dimension_to_port = test_value
        self.assertEqual(self.instance.dimension_to_port, test_value)
    
    def test_dimension_to_starboard_property(self):
        """
        Test dimension_to_starboard property
        """
        test_value = int(92)
        self.instance.dimension_to_starboard = test_value
        self.assertEqual(self.instance.dimension_to_starboard, test_value)
    
    def test_draught_property(self):
        """
        Test draught property
        """
        test_value = float(18.983977035719303)
        self.instance.draught = test_value
        self.assertEqual(self.instance.draught, test_value)
    
    def test_destination_property(self):
        """
        Test destination property
        """
        test_value = 'htzmuemrrtysqbdqqzxs'
        self.instance.destination = test_value
        self.assertEqual(self.instance.destination, test_value)
    
    def test_eta_month_property(self):
        """
        Test eta_month property
        """
        test_value = int(77)
        self.instance.eta_month = test_value
        self.assertEqual(self.instance.eta_month, test_value)
    
    def test_eta_day_property(self):
        """
        Test eta_day property
        """
        test_value = int(47)
        self.instance.eta_day = test_value
        self.assertEqual(self.instance.eta_day, test_value)
    
    def test_eta_hour_property(self):
        """
        Test eta_hour property
        """
        test_value = int(71)
        self.instance.eta_hour = test_value
        self.assertEqual(self.instance.eta_hour, test_value)
    
    def test_eta_minute_property(self):
        """
        Test eta_minute property
        """
        test_value = int(97)
        self.instance.eta_minute = test_value
        self.assertEqual(self.instance.eta_minute, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'rohsxlbvfrnutyzhwarb'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'odeeaghohrulnxxzgmga'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = StaticVoyageData.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = StaticVoyageData.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

