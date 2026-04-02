"""
Test case for PositionReportClassB
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from kystverket_ais_producer_data.no.kystverket.ais.positionreportclassb import PositionReportClassB


class Test_PositionReportClassB(unittest.TestCase):
    """
    Test case for PositionReportClassB
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_PositionReportClassB.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of PositionReportClassB for testing
        """
        instance = PositionReportClassB(
            mmsi=int(8),
            speed_over_ground=float(17.023667720756375),
            position_accuracy=int(77),
            longitude=float(22.79905146818266),
            latitude=float(98.87904337769517),
            course_over_ground=float(25.748487238502904),
            true_heading=int(53),
            timestamp='xxgfhmlwhvyvnrcfxhuc',
            station_id='klxjtgbchyomqbjsyfco',
            msg_type=int(71)
        )
        return instance

    
    def test_mmsi_property(self):
        """
        Test mmsi property
        """
        test_value = int(8)
        self.instance.mmsi = test_value
        self.assertEqual(self.instance.mmsi, test_value)
    
    def test_speed_over_ground_property(self):
        """
        Test speed_over_ground property
        """
        test_value = float(17.023667720756375)
        self.instance.speed_over_ground = test_value
        self.assertEqual(self.instance.speed_over_ground, test_value)
    
    def test_position_accuracy_property(self):
        """
        Test position_accuracy property
        """
        test_value = int(77)
        self.instance.position_accuracy = test_value
        self.assertEqual(self.instance.position_accuracy, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(22.79905146818266)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(98.87904337769517)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_course_over_ground_property(self):
        """
        Test course_over_ground property
        """
        test_value = float(25.748487238502904)
        self.instance.course_over_ground = test_value
        self.assertEqual(self.instance.course_over_ground, test_value)
    
    def test_true_heading_property(self):
        """
        Test true_heading property
        """
        test_value = int(53)
        self.instance.true_heading = test_value
        self.assertEqual(self.instance.true_heading, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'xxgfhmlwhvyvnrcfxhuc'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'klxjtgbchyomqbjsyfco'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_msg_type_property(self):
        """
        Test msg_type property
        """
        test_value = int(71)
        self.instance.msg_type = test_value
        self.assertEqual(self.instance.msg_type, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = PositionReportClassB.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
