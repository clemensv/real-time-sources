"""
Test case for ShipStatic
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from aisstream_amqp_producer_data.shipstatic import ShipStatic
from aisstream_amqp_producer_data.msgtypeenum import MsgTypeenum


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
            mmsi='zddwwbrzqowjxrtruqia',
            flag='yrxjpsmqegvvolaylsru',
            ship_type='tyjmgtgavnctsnbjrwam',
            geohash5='rdktadnlploutrnofgnj',
            msg_type=MsgTypeenum.position_report,
            user_id=int(79),
            name='hghrllfmepzbvolutzyo',
            call_sign='nqoovjfsagkwqzwdlnjp',
            imo_number=int(1),
            ship_type_code=int(74),
            destination='rzvvgqcfdvzegvnyokcb',
            eta='ukwhhjgtsqboyubdqnio',
            draught=float(80.49629100549164),
            dim_to_bow=int(21),
            dim_to_stern=int(95),
            dim_to_port=int(46),
            dim_to_starboard=int(57),
            message_id=int(50)
        )
        return instance

    
    def test_mmsi_property(self):
        """
        Test mmsi property
        """
        test_value = 'zddwwbrzqowjxrtruqia'
        self.instance.mmsi = test_value
        self.assertEqual(self.instance.mmsi, test_value)
    
    def test_flag_property(self):
        """
        Test flag property
        """
        test_value = 'yrxjpsmqegvvolaylsru'
        self.instance.flag = test_value
        self.assertEqual(self.instance.flag, test_value)
    
    def test_ship_type_property(self):
        """
        Test ship_type property
        """
        test_value = 'tyjmgtgavnctsnbjrwam'
        self.instance.ship_type = test_value
        self.assertEqual(self.instance.ship_type, test_value)
    
    def test_geohash5_property(self):
        """
        Test geohash5 property
        """
        test_value = 'rdktadnlploutrnofgnj'
        self.instance.geohash5 = test_value
        self.assertEqual(self.instance.geohash5, test_value)
    
    def test_msg_type_property(self):
        """
        Test msg_type property
        """
        test_value = MsgTypeenum.position_report
        self.instance.msg_type = test_value
        self.assertEqual(self.instance.msg_type, test_value)
    
    def test_user_id_property(self):
        """
        Test user_id property
        """
        test_value = int(79)
        self.instance.user_id = test_value
        self.assertEqual(self.instance.user_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'hghrllfmepzbvolutzyo'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_call_sign_property(self):
        """
        Test call_sign property
        """
        test_value = 'nqoovjfsagkwqzwdlnjp'
        self.instance.call_sign = test_value
        self.assertEqual(self.instance.call_sign, test_value)
    
    def test_imo_number_property(self):
        """
        Test imo_number property
        """
        test_value = int(1)
        self.instance.imo_number = test_value
        self.assertEqual(self.instance.imo_number, test_value)
    
    def test_ship_type_code_property(self):
        """
        Test ship_type_code property
        """
        test_value = int(74)
        self.instance.ship_type_code = test_value
        self.assertEqual(self.instance.ship_type_code, test_value)
    
    def test_destination_property(self):
        """
        Test destination property
        """
        test_value = 'rzvvgqcfdvzegvnyokcb'
        self.instance.destination = test_value
        self.assertEqual(self.instance.destination, test_value)
    
    def test_eta_property(self):
        """
        Test eta property
        """
        test_value = 'ukwhhjgtsqboyubdqnio'
        self.instance.eta = test_value
        self.assertEqual(self.instance.eta, test_value)
    
    def test_draught_property(self):
        """
        Test draught property
        """
        test_value = float(80.49629100549164)
        self.instance.draught = test_value
        self.assertEqual(self.instance.draught, test_value)
    
    def test_dim_to_bow_property(self):
        """
        Test dim_to_bow property
        """
        test_value = int(21)
        self.instance.dim_to_bow = test_value
        self.assertEqual(self.instance.dim_to_bow, test_value)
    
    def test_dim_to_stern_property(self):
        """
        Test dim_to_stern property
        """
        test_value = int(95)
        self.instance.dim_to_stern = test_value
        self.assertEqual(self.instance.dim_to_stern, test_value)
    
    def test_dim_to_port_property(self):
        """
        Test dim_to_port property
        """
        test_value = int(46)
        self.instance.dim_to_port = test_value
        self.assertEqual(self.instance.dim_to_port, test_value)
    
    def test_dim_to_starboard_property(self):
        """
        Test dim_to_starboard property
        """
        test_value = int(57)
        self.instance.dim_to_starboard = test_value
        self.assertEqual(self.instance.dim_to_starboard, test_value)
    
    def test_message_id_property(self):
        """
        Test message_id property
        """
        test_value = int(50)
        self.instance.message_id = test_value
        self.assertEqual(self.instance.message_id, test_value)
    
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

