"""
Test case for PositionReport
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from kystverket_ais_producer_data.positionreport import PositionReport
from kystverket_ais_producer_data.msgtypeenum import MsgTypeenum


class Test_PositionReport(unittest.TestCase):
    """
    Test case for PositionReport
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_PositionReport.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of PositionReport for testing
        """
        instance = PositionReport(
            mmsi='joxibnvoityzjzkeshph',
            flag='blkvvcraahrbqjklucgd',
            ship_type='exoiimilpjzzejggzhgv',
            geohash5='zoyekdfiozxfzvlydvsx',
            msg_type=MsgTypeenum.position_MINUSreport,
            latitude=float(48.167497167755904),
            longitude=float(65.74085291593907),
            speed_over_ground=float(25.399953755233827),
            course_over_ground=float(15.054427283591487),
            true_heading=int(21),
            navigation_status=int(59),
            rate_of_turn=float(38.056320592128365),
            position_accuracy=int(65),
            timestamp='cgqnkfrdggohwikxucgg',
            station_id='rfihobnjmblxzabgdjwq',
            ais_msg_type=int(19)
        )
        return instance

    
    def test_mmsi_property(self):
        """
        Test mmsi property
        """
        test_value = 'joxibnvoityzjzkeshph'
        self.instance.mmsi = test_value
        self.assertEqual(self.instance.mmsi, test_value)
    
    def test_flag_property(self):
        """
        Test flag property
        """
        test_value = 'blkvvcraahrbqjklucgd'
        self.instance.flag = test_value
        self.assertEqual(self.instance.flag, test_value)
    
    def test_ship_type_property(self):
        """
        Test ship_type property
        """
        test_value = 'exoiimilpjzzejggzhgv'
        self.instance.ship_type = test_value
        self.assertEqual(self.instance.ship_type, test_value)
    
    def test_geohash5_property(self):
        """
        Test geohash5 property
        """
        test_value = 'zoyekdfiozxfzvlydvsx'
        self.instance.geohash5 = test_value
        self.assertEqual(self.instance.geohash5, test_value)
    
    def test_msg_type_property(self):
        """
        Test msg_type property
        """
        test_value = MsgTypeenum.position_MINUSreport
        self.instance.msg_type = test_value
        self.assertEqual(self.instance.msg_type, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(48.167497167755904)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(65.74085291593907)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_speed_over_ground_property(self):
        """
        Test speed_over_ground property
        """
        test_value = float(25.399953755233827)
        self.instance.speed_over_ground = test_value
        self.assertEqual(self.instance.speed_over_ground, test_value)
    
    def test_course_over_ground_property(self):
        """
        Test course_over_ground property
        """
        test_value = float(15.054427283591487)
        self.instance.course_over_ground = test_value
        self.assertEqual(self.instance.course_over_ground, test_value)
    
    def test_true_heading_property(self):
        """
        Test true_heading property
        """
        test_value = int(21)
        self.instance.true_heading = test_value
        self.assertEqual(self.instance.true_heading, test_value)
    
    def test_navigation_status_property(self):
        """
        Test navigation_status property
        """
        test_value = int(59)
        self.instance.navigation_status = test_value
        self.assertEqual(self.instance.navigation_status, test_value)
    
    def test_rate_of_turn_property(self):
        """
        Test rate_of_turn property
        """
        test_value = float(38.056320592128365)
        self.instance.rate_of_turn = test_value
        self.assertEqual(self.instance.rate_of_turn, test_value)
    
    def test_position_accuracy_property(self):
        """
        Test position_accuracy property
        """
        test_value = int(65)
        self.instance.position_accuracy = test_value
        self.assertEqual(self.instance.position_accuracy, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'cgqnkfrdggohwikxucgg'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'rfihobnjmblxzabgdjwq'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_ais_msg_type_property(self):
        """
        Test ais_msg_type property
        """
        test_value = int(19)
        self.instance.ais_msg_type = test_value
        self.assertEqual(self.instance.ais_msg_type, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = PositionReport.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = PositionReport.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

