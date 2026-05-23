"""
Test case for ShipStatic
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from kystverket_ais_mqtt_producer_data.shipstatic import ShipStatic
from kystverket_ais_mqtt_producer_data.msgtypeenum import MsgTypeenum


class Test_ShipStatic(unittest.TestCase):
    """
    Test case for ShipStatic
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_ShipStatic.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of ShipStatic for testing
        """
        instance = ShipStatic(
            mmsi='jffcsnjbkffpoenigsia',
            flag='gptrmtbtewawlqszmrka',
            ship_type='lvbwibwgmetkybjdchyh',
            geohash5='esuwcryrpzzffuedxdfj',
            msg_type=MsgTypeenum.position_report,
            ship_name='dftqqaqhnlhypxveczjk',
            callsign='kispfiswecnnkkztbhbh',
            imo_number=int(92),
            ship_type_code=int(24),
            destination='rfmttkwvmyjgjdwapujq',
            eta='qzqltzdlasqxcjrqipwh',
            draught=float(42.95389116507108),
            dim_to_bow=int(81),
            dim_to_stern=int(10),
            dim_to_port=int(95),
            dim_to_starboard=int(94),
            timestamp='tdywtqglsttlglhlaumt',
            station_id='hlaanzewhevwmosyzvnv',
            ais_msg_type=int(94)
        )
        return instance

    
    def test_mmsi_property(self):
        """
        Test mmsi property
        """
        test_value = 'jffcsnjbkffpoenigsia'
        self.instance.mmsi = test_value
        self.assertEqual(self.instance.mmsi, test_value)
    
    def test_flag_property(self):
        """
        Test flag property
        """
        test_value = 'gptrmtbtewawlqszmrka'
        self.instance.flag = test_value
        self.assertEqual(self.instance.flag, test_value)
    
    def test_ship_type_property(self):
        """
        Test ship_type property
        """
        test_value = 'lvbwibwgmetkybjdchyh'
        self.instance.ship_type = test_value
        self.assertEqual(self.instance.ship_type, test_value)
    
    def test_geohash5_property(self):
        """
        Test geohash5 property
        """
        test_value = 'esuwcryrpzzffuedxdfj'
        self.instance.geohash5 = test_value
        self.assertEqual(self.instance.geohash5, test_value)
    
    def test_msg_type_property(self):
        """
        Test msg_type property
        """
        test_value = MsgTypeenum.position_report
        self.instance.msg_type = test_value
        self.assertEqual(self.instance.msg_type, test_value)
    
    def test_ship_name_property(self):
        """
        Test ship_name property
        """
        test_value = 'dftqqaqhnlhypxveczjk'
        self.instance.ship_name = test_value
        self.assertEqual(self.instance.ship_name, test_value)
    
    def test_callsign_property(self):
        """
        Test callsign property
        """
        test_value = 'kispfiswecnnkkztbhbh'
        self.instance.callsign = test_value
        self.assertEqual(self.instance.callsign, test_value)
    
    def test_imo_number_property(self):
        """
        Test imo_number property
        """
        test_value = int(92)
        self.instance.imo_number = test_value
        self.assertEqual(self.instance.imo_number, test_value)
    
    def test_ship_type_code_property(self):
        """
        Test ship_type_code property
        """
        test_value = int(24)
        self.instance.ship_type_code = test_value
        self.assertEqual(self.instance.ship_type_code, test_value)
    
    def test_destination_property(self):
        """
        Test destination property
        """
        test_value = 'rfmttkwvmyjgjdwapujq'
        self.instance.destination = test_value
        self.assertEqual(self.instance.destination, test_value)
    
    def test_eta_property(self):
        """
        Test eta property
        """
        test_value = 'qzqltzdlasqxcjrqipwh'
        self.instance.eta = test_value
        self.assertEqual(self.instance.eta, test_value)
    
    def test_draught_property(self):
        """
        Test draught property
        """
        test_value = float(42.95389116507108)
        self.instance.draught = test_value
        self.assertEqual(self.instance.draught, test_value)
    
    def test_dim_to_bow_property(self):
        """
        Test dim_to_bow property
        """
        test_value = int(81)
        self.instance.dim_to_bow = test_value
        self.assertEqual(self.instance.dim_to_bow, test_value)
    
    def test_dim_to_stern_property(self):
        """
        Test dim_to_stern property
        """
        test_value = int(10)
        self.instance.dim_to_stern = test_value
        self.assertEqual(self.instance.dim_to_stern, test_value)
    
    def test_dim_to_port_property(self):
        """
        Test dim_to_port property
        """
        test_value = int(95)
        self.instance.dim_to_port = test_value
        self.assertEqual(self.instance.dim_to_port, test_value)
    
    def test_dim_to_starboard_property(self):
        """
        Test dim_to_starboard property
        """
        test_value = int(94)
        self.instance.dim_to_starboard = test_value
        self.assertEqual(self.instance.dim_to_starboard, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'tdywtqglsttlglhlaumt'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'hlaanzewhevwmosyzvnv'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_ais_msg_type_property(self):
        """
        Test ais_msg_type property
        """
        test_value = int(94)
        self.instance.ais_msg_type = test_value
        self.assertEqual(self.instance.ais_msg_type, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = ShipStatic.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = ShipStatic.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

