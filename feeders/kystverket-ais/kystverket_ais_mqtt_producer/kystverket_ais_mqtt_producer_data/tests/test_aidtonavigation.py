"""
Test case for AidToNavigation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from kystverket_ais_mqtt_producer_data.aidtonavigation import AidToNavigation
from kystverket_ais_mqtt_producer_data.msgtypeenum import MsgTypeenum


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
            mmsi='rldbhodgdtfszbynuiqw',
            flag='hynwsjayafykjpwerfar',
            ship_type='vhncldtecqnfvyvqidnm',
            geohash5='svotwvighvbzcdhzwlrk',
            msg_type=MsgTypeenum.position_report,
            name='xizexrtivwdohxadqynk',
            aid_type=int(87),
            latitude=float(60.04337243353515),
            longitude=float(16.89877298713407),
            position_accuracy=int(4),
            timestamp='fsrouukiwpmrghikkhin',
            station_id='negftnhjsgsreibzgegz',
            ais_msg_type=int(60)
        )
        return instance

    
    def test_mmsi_property(self):
        """
        Test mmsi property
        """
        test_value = 'rldbhodgdtfszbynuiqw'
        self.instance.mmsi = test_value
        self.assertEqual(self.instance.mmsi, test_value)
    
    def test_flag_property(self):
        """
        Test flag property
        """
        test_value = 'hynwsjayafykjpwerfar'
        self.instance.flag = test_value
        self.assertEqual(self.instance.flag, test_value)
    
    def test_ship_type_property(self):
        """
        Test ship_type property
        """
        test_value = 'vhncldtecqnfvyvqidnm'
        self.instance.ship_type = test_value
        self.assertEqual(self.instance.ship_type, test_value)
    
    def test_geohash5_property(self):
        """
        Test geohash5 property
        """
        test_value = 'svotwvighvbzcdhzwlrk'
        self.instance.geohash5 = test_value
        self.assertEqual(self.instance.geohash5, test_value)
    
    def test_msg_type_property(self):
        """
        Test msg_type property
        """
        test_value = MsgTypeenum.position_report
        self.instance.msg_type = test_value
        self.assertEqual(self.instance.msg_type, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'xizexrtivwdohxadqynk'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_aid_type_property(self):
        """
        Test aid_type property
        """
        test_value = int(87)
        self.instance.aid_type = test_value
        self.assertEqual(self.instance.aid_type, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(60.04337243353515)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(16.89877298713407)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_position_accuracy_property(self):
        """
        Test position_accuracy property
        """
        test_value = int(4)
        self.instance.position_accuracy = test_value
        self.assertEqual(self.instance.position_accuracy, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'fsrouukiwpmrghikkhin'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'negftnhjsgsreibzgegz'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_ais_msg_type_property(self):
        """
        Test ais_msg_type property
        """
        test_value = int(60)
        self.instance.ais_msg_type = test_value
        self.assertEqual(self.instance.ais_msg_type, test_value)
    
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

