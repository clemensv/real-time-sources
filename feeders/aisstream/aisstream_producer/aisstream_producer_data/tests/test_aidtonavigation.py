"""
Test case for AidToNavigation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from aisstream_producer_data.aidtonavigation import AidToNavigation
from aisstream_producer_data.msgtypeenum import MsgTypeenum


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
            mmsi='ecituedkuulttrdnverf',
            flag='yyoghsfitcovaxlqchjn',
            ship_type='shyvfhgxirkdrrelfqdb',
            geohash5='xxjxarioeclbhqdhxlcp',
            msg_type=MsgTypeenum.position_MINUSreport,
            user_id=int(86),
            name='eduylvxkvjdwkwnmbjxp',
            type=int(60),
            latitude=float(85.51654472156446),
            longitude=float(13.057253231392153),
            off_position=False,
            virtual_atoN=False,
            message_id=int(80)
        )
        return instance

    
    def test_mmsi_property(self):
        """
        Test mmsi property
        """
        test_value = 'ecituedkuulttrdnverf'
        self.instance.mmsi = test_value
        self.assertEqual(self.instance.mmsi, test_value)
    
    def test_flag_property(self):
        """
        Test flag property
        """
        test_value = 'yyoghsfitcovaxlqchjn'
        self.instance.flag = test_value
        self.assertEqual(self.instance.flag, test_value)
    
    def test_ship_type_property(self):
        """
        Test ship_type property
        """
        test_value = 'shyvfhgxirkdrrelfqdb'
        self.instance.ship_type = test_value
        self.assertEqual(self.instance.ship_type, test_value)
    
    def test_geohash5_property(self):
        """
        Test geohash5 property
        """
        test_value = 'xxjxarioeclbhqdhxlcp'
        self.instance.geohash5 = test_value
        self.assertEqual(self.instance.geohash5, test_value)
    
    def test_msg_type_property(self):
        """
        Test msg_type property
        """
        test_value = MsgTypeenum.position_MINUSreport
        self.instance.msg_type = test_value
        self.assertEqual(self.instance.msg_type, test_value)
    
    def test_user_id_property(self):
        """
        Test user_id property
        """
        test_value = int(86)
        self.instance.user_id = test_value
        self.assertEqual(self.instance.user_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'eduylvxkvjdwkwnmbjxp'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_type_property(self):
        """
        Test type property
        """
        test_value = int(60)
        self.instance.type = test_value
        self.assertEqual(self.instance.type, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(85.51654472156446)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(13.057253231392153)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_off_position_property(self):
        """
        Test off_position property
        """
        test_value = False
        self.instance.off_position = test_value
        self.assertEqual(self.instance.off_position, test_value)
    
    def test_virtual_atoN_property(self):
        """
        Test virtual_atoN property
        """
        test_value = False
        self.instance.virtual_atoN = test_value
        self.assertEqual(self.instance.virtual_atoN, test_value)
    
    def test_message_id_property(self):
        """
        Test message_id property
        """
        test_value = int(80)
        self.instance.message_id = test_value
        self.assertEqual(self.instance.message_id, test_value)
    
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

