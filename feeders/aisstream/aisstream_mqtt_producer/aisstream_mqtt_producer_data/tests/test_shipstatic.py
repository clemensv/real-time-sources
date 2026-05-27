"""
Test case for ShipStatic
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from aisstream_mqtt_producer_data.shipstatic import ShipStatic
from aisstream_mqtt_producer_data.msgtypeenum import MsgTypeenum


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
            mmsi='dgttqohothdpumyhwntc',
            flag='zlvgsayepnrxbcltdspz',
            ship_type='qdcckobwdlbumdekeeox',
            geohash5='cnkkddmfddmompkjwdlu',
            msg_type=MsgTypeenum.position_report,
            user_id=int(2),
            name='diojbbfhxuugmhclmfsi',
            call_sign='rrdyoybhiriwnegogseb',
            imo_number=int(63),
            ship_type_code=int(77),
            destination='zpqsfwhcuvlcpegdykym',
            eta='nyqkvvhdpfrxhqzcsqfi',
            draught=float(25.388484484238848),
            dim_to_bow=int(28),
            dim_to_stern=int(0),
            dim_to_port=int(6),
            dim_to_starboard=int(75),
            message_id=int(3)
        )
        return instance

    
    def test_mmsi_property(self):
        """
        Test mmsi property
        """
        test_value = 'dgttqohothdpumyhwntc'
        self.instance.mmsi = test_value
        self.assertEqual(self.instance.mmsi, test_value)
    
    def test_flag_property(self):
        """
        Test flag property
        """
        test_value = 'zlvgsayepnrxbcltdspz'
        self.instance.flag = test_value
        self.assertEqual(self.instance.flag, test_value)
    
    def test_ship_type_property(self):
        """
        Test ship_type property
        """
        test_value = 'qdcckobwdlbumdekeeox'
        self.instance.ship_type = test_value
        self.assertEqual(self.instance.ship_type, test_value)
    
    def test_geohash5_property(self):
        """
        Test geohash5 property
        """
        test_value = 'cnkkddmfddmompkjwdlu'
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
        test_value = int(2)
        self.instance.user_id = test_value
        self.assertEqual(self.instance.user_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'diojbbfhxuugmhclmfsi'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_call_sign_property(self):
        """
        Test call_sign property
        """
        test_value = 'rrdyoybhiriwnegogseb'
        self.instance.call_sign = test_value
        self.assertEqual(self.instance.call_sign, test_value)
    
    def test_imo_number_property(self):
        """
        Test imo_number property
        """
        test_value = int(63)
        self.instance.imo_number = test_value
        self.assertEqual(self.instance.imo_number, test_value)
    
    def test_ship_type_code_property(self):
        """
        Test ship_type_code property
        """
        test_value = int(77)
        self.instance.ship_type_code = test_value
        self.assertEqual(self.instance.ship_type_code, test_value)
    
    def test_destination_property(self):
        """
        Test destination property
        """
        test_value = 'zpqsfwhcuvlcpegdykym'
        self.instance.destination = test_value
        self.assertEqual(self.instance.destination, test_value)
    
    def test_eta_property(self):
        """
        Test eta property
        """
        test_value = 'nyqkvvhdpfrxhqzcsqfi'
        self.instance.eta = test_value
        self.assertEqual(self.instance.eta, test_value)
    
    def test_draught_property(self):
        """
        Test draught property
        """
        test_value = float(25.388484484238848)
        self.instance.draught = test_value
        self.assertEqual(self.instance.draught, test_value)
    
    def test_dim_to_bow_property(self):
        """
        Test dim_to_bow property
        """
        test_value = int(28)
        self.instance.dim_to_bow = test_value
        self.assertEqual(self.instance.dim_to_bow, test_value)
    
    def test_dim_to_stern_property(self):
        """
        Test dim_to_stern property
        """
        test_value = int(0)
        self.instance.dim_to_stern = test_value
        self.assertEqual(self.instance.dim_to_stern, test_value)
    
    def test_dim_to_port_property(self):
        """
        Test dim_to_port property
        """
        test_value = int(6)
        self.instance.dim_to_port = test_value
        self.assertEqual(self.instance.dim_to_port, test_value)
    
    def test_dim_to_starboard_property(self):
        """
        Test dim_to_starboard property
        """
        test_value = int(75)
        self.instance.dim_to_starboard = test_value
        self.assertEqual(self.instance.dim_to_starboard, test_value)
    
    def test_message_id_property(self):
        """
        Test message_id property
        """
        test_value = int(3)
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

