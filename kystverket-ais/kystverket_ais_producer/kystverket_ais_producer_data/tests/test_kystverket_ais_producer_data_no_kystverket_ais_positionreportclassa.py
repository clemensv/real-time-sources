"""
Test case for PositionReportClassA
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from kystverket_ais_producer_data.no.kystverket.ais.positionreportclassa import PositionReportClassA


class Test_PositionReportClassA(unittest.TestCase):
    """
    Test case for PositionReportClassA
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_PositionReportClassA.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of PositionReportClassA for testing
        """
        instance = PositionReportClassA(
            mmsi=int(2),
            navigation_status=int(48),
            rate_of_turn=float(69.11465756350435),
            speed_over_ground=float(24.985209876611936),
            position_accuracy=int(46),
            longitude=float(48.496521465812435),
            latitude=float(93.48743589489867),
            course_over_ground=float(68.4564759019014),
            true_heading=int(50),
            timestamp='bkjktwskctpnhlhfymvc',
            station_id='xibvxtcslmguoupdpvsc',
            msg_type=int(15)
        )
        return instance

    
    def test_mmsi_property(self):
        """
        Test mmsi property
        """
        test_value = int(2)
        self.instance.mmsi = test_value
        self.assertEqual(self.instance.mmsi, test_value)
    
    def test_navigation_status_property(self):
        """
        Test navigation_status property
        """
        test_value = int(48)
        self.instance.navigation_status = test_value
        self.assertEqual(self.instance.navigation_status, test_value)
    
    def test_rate_of_turn_property(self):
        """
        Test rate_of_turn property
        """
        test_value = float(69.11465756350435)
        self.instance.rate_of_turn = test_value
        self.assertEqual(self.instance.rate_of_turn, test_value)
    
    def test_speed_over_ground_property(self):
        """
        Test speed_over_ground property
        """
        test_value = float(24.985209876611936)
        self.instance.speed_over_ground = test_value
        self.assertEqual(self.instance.speed_over_ground, test_value)
    
    def test_position_accuracy_property(self):
        """
        Test position_accuracy property
        """
        test_value = int(46)
        self.instance.position_accuracy = test_value
        self.assertEqual(self.instance.position_accuracy, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(48.496521465812435)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(93.48743589489867)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_course_over_ground_property(self):
        """
        Test course_over_ground property
        """
        test_value = float(68.4564759019014)
        self.instance.course_over_ground = test_value
        self.assertEqual(self.instance.course_over_ground, test_value)
    
    def test_true_heading_property(self):
        """
        Test true_heading property
        """
        test_value = int(50)
        self.instance.true_heading = test_value
        self.assertEqual(self.instance.true_heading, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'bkjktwskctpnhlhfymvc'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'xibvxtcslmguoupdpvsc'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_msg_type_property(self):
        """
        Test msg_type property
        """
        test_value = int(15)
        self.instance.msg_type = test_value
        self.assertEqual(self.instance.msg_type, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = PositionReportClassA.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
