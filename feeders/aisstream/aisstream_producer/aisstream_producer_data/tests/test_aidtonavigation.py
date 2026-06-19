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
            mmsi='asvdqdsriggfytvoctlf',
            flag='lhyhxttubjokjwxuhivz',
            ship_type='vtonwtmzrtyaxbzpfueq',
            geohash5='ftbkwrxllyphtmhifrkd',
            msg_type=MsgTypeenum.position_MINUSreport,
            user_id=int(79),
            name='jbtvhkumgapkhtdompcl',
            type=int(85),
            latitude=float(81.34505560143803),
            longitude=float(14.259890561055377),
            off_position=True,
            virtual_atoN=False,
            message_id=int(26)
        )
        return instance

    
    def test_mmsi_property(self):
        """
        Test mmsi property
        """
        test_value = 'asvdqdsriggfytvoctlf'
        self.instance.mmsi = test_value
        self.assertEqual(self.instance.mmsi, test_value)
    
    def test_flag_property(self):
        """
        Test flag property
        """
        test_value = 'lhyhxttubjokjwxuhivz'
        self.instance.flag = test_value
        self.assertEqual(self.instance.flag, test_value)
    
    def test_ship_type_property(self):
        """
        Test ship_type property
        """
        test_value = 'vtonwtmzrtyaxbzpfueq'
        self.instance.ship_type = test_value
        self.assertEqual(self.instance.ship_type, test_value)
    
    def test_geohash5_property(self):
        """
        Test geohash5 property
        """
        test_value = 'ftbkwrxllyphtmhifrkd'
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
        test_value = int(79)
        self.instance.user_id = test_value
        self.assertEqual(self.instance.user_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'jbtvhkumgapkhtdompcl'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_type_property(self):
        """
        Test type property
        """
        test_value = int(85)
        self.instance.type = test_value
        self.assertEqual(self.instance.type, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(81.34505560143803)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(14.259890561055377)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_off_position_property(self):
        """
        Test off_position property
        """
        test_value = True
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
        test_value = int(26)
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

